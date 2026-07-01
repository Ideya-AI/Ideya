"""Moving anonymous (session-keyed) participation onto a user account.

Decision B (hybrid): readers participate anonymously via their session; when
they sign up or log in, that session's rows become theirs. Django cycles the
session key on login, so callers must capture the key *before* authenticating.
"""

from django.db import transaction
from django.db.models import F

from .models import Position, Question, Response, Stance, Submission, Vote


@transaction.atomic
def merge_session_participation(user, session_key):
    if not session_key:
        return

    # Votes — the user's existing vote wins; a session duplicate is removed
    # and its cached count undone (each row incremented the counter once).
    for vote in Vote.objects.filter(session_key=session_key, user__isnull=True):
        if vote.question_id:
            duplicate = Vote.objects.filter(user=user, question_id=vote.question_id)
        else:
            duplicate = Vote.objects.filter(user=user, position_id=vote.position_id)
        if duplicate.exists():
            if vote.question_id:
                Question.objects.filter(pk=vote.question_id).update(
                    votes=F("votes") - 1
                )
            else:
                Position.objects.filter(pk=vote.position_id).update(
                    importance=F("importance") - 1
                )
            vote.delete()
        else:
            vote.user = user
            vote.session_key = ""
            vote.save(update_fields=["user", "session_key"])

    # Stances — the session stance is the fresher signal, so it wins.
    for stance in Stance.objects.filter(session_key=session_key, user__isnull=True):
        existing = Stance.objects.filter(user=user, position=stance.position).first()
        if existing:
            if existing.value != stance.value:
                existing.value = stance.value
                existing.save(update_fields=["value", "updated_at"])
            stance.delete()
        else:
            stance.user = user
            stance.session_key = ""
            stance.save(update_fields=["user", "session_key"])

    # Prompt responses — like stances, the session answer is the fresher signal,
    # so it wins: drop any earlier answer the user gave to the same prompt, then
    # promote the session row.
    for response in Response.objects.filter(session_key=session_key, user__isnull=True):
        Response.objects.filter(user=user, prompt_id=response.prompt_id).delete()
        response.user = user
        response.session_key = ""
        response.save(update_fields=["user", "session_key"])

    Submission.objects.filter(session_key=session_key, user__isnull=True).update(
        user=user, session_key=""
    )


@transaction.atomic
def retract_user_participation(user):
    """Undo the cached counters for a user's votes (called before account
    deletion — the rows themselves cascade away with the user)."""
    for vote in Vote.objects.filter(user=user):
        if vote.question_id:
            Question.objects.filter(pk=vote.question_id).update(votes=F("votes") - 1)
        else:
            Position.objects.filter(pk=vote.position_id).update(
                importance=F("importance") - 1
            )

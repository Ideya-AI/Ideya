from django.db import models


class Topic(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    summary = models.CharField(
        max_length=400,
        blank=True,
        help_text="One-sentence framing shown above the layer toggle.",
    )

    l1_content = models.TextField(
        blank=True,
        help_text="L1 — infographic-level overview. HTML/SVG allowed.",
    )
    l2_content = models.TextField(
        blank=True,
        help_text="L2 — comprehensive long-form.",
    )
    l3_content = models.TextField(
        blank=True,
        help_text="L3 — annotated external learning map.",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["title"]

    def __str__(self) -> str:
        return self.title


class TopicEdge(models.Model):
    DEPENDS_ON = "depends_on"
    RELATES_TO = "relates_to"
    EDGE_TYPES = [
        (DEPENDS_ON, "Depends on"),
        (RELATES_TO, "Relates to"),
    ]

    source = models.ForeignKey(
        Topic, related_name="outgoing_edges", on_delete=models.CASCADE
    )
    target = models.ForeignKey(
        Topic, related_name="incoming_edges", on_delete=models.CASCADE
    )
    kind = models.CharField(max_length=20, choices=EDGE_TYPES, default=RELATES_TO)
    note = models.CharField(max_length=300, blank=True)

    class Meta:
        unique_together = [("source", "target", "kind")]

    def __str__(self) -> str:
        return f"{self.source} -[{self.kind}]-> {self.target}"

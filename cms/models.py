from __future__ import unicode_literals

from django.db import models

from django.utils.safestring import mark_safe
from django.template.response import TemplateResponse

from modelcluster.fields import ParentalKey
from modelcluster.tags import ClusterTaggableManager
from modelcluster.models import ClusterableModel

from django.shortcuts import render
from wagtail.wagtailcore.models import Page, Orderable, Site
from wagtail.wagtailcore.fields import RichTextField, StreamField
from wagtail.wagtailcore.blocks import ChoiceBlock, TextBlock, ChooserBlock, StructBlock, ListBlock, StreamBlock, FieldBlock, CharBlock, RichTextBlock, PageChooserBlock, RawHTMLBlock
from wagtail.wagtailadmin.edit_handlers import (FieldPanel,
                                                InlinePanel,
                                                MultiFieldPanel,
                                                PageChooserPanel,
                                                StreamFieldPanel,)
from wagtail.contrib.wagtailroutablepage.models import RoutablePageMixin, route
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailimages.blocks import ImageChooserBlock
from wagtail.wagtailsearch import index
from wagtail.wagtailsnippets.models import register_snippet

class HomePage(Page):
    intro_text = models.CharField(max_length=255, blank=True, null=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro_text'),
    ]

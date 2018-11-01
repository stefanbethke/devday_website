from django.db.models import Q
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import ValidationError
from django.core.mail import EmailMultiAlternatives
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from html2text import HTML2Text

from attendee.views import StaffUserMixin
from event.models import Event
from speaker.models import PublishedSpeaker, Speaker
from talk.models import Attendee

from .forms import SendEmailForm

User = get_user_model()


def exception_test_view(request):
    raise Exception("Synthetic server error")


class DevDayEmailMessage(EmailMultiAlternatives):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.recipientlist = []

    def recipients(self):
        return self.recipientlist


class DevDayEmailRecipients:
    def get_form_choices(self):
        return [(k, self.choices[k]['label']) for k in self.choices.keys()]

    def get_email_addresses(self, choice):
        if choice not in self.choices:
            raise ValidationError(f'Unknown recipient selector {choice}')
        return self.choices[choice]['q']()

    def get_choice_label(self, choice):
        if choice not in self.choices:
            raise ValidationError(f'Unknown recipient selector {choice}')
        return self.choices[choice]['label']

    def choice_all_attendees(self):
        users = User.objects.filter(
            Q(contact_permission_date__isnull=False)
            | Q(attendees__event=Event.objects.current_event())
        ).filter(is_active=True).order_by('email').distinct()
        return [u.email for u in users]

    def choice_attendees(self):
        attendees = Attendee.objects.filter(
            event_id=Event.objects.current_event_id(),
            user__is_active=True
        ).order_by("user__email")
        return [a.user.email for a in attendees]

    def choice_inactive_attendees(self):
        attendees = Attendee.objects.filter(
            event_id=Event.objects.current_event_id(),
            user__is_active=False
        ).order_by("user__email")
        return [a.user.email for a in attendees]

    def choice_draft_speakers(self):
        speakers = Speaker.objects.filter(
            talk__event=Event.objects.current_event(),
            user__is_active=True
        ).order_by("user__email").distinct()
        return [s.user.email for s in speakers]

    def choice_published_speakers(self):
        speakers = PublishedSpeaker.objects.filter(
            talk__event=Event.objects.current_event(),
            speaker__user__is_active=True
        ).order_by("speaker__user__email").distinct()
        return [s.speaker.user.email for s in speakers]

    def __init__(self):
        self.choices = {}
        self.choices['users'] = {
            'label': _('past and present attendees'),
            'q': self.choice_all_attendees}
        self.choices['attendees'] = {
            'label': _('current attendees'),
            'q': self.choice_attendees}
        self.choices['inactive_attendees'] = {
            'label': _('registered but inactive attendees'),
            'q': self.choice_inactive_attendees}
        self.choices['draft_speakers'] = {
            'label': _('candidate speakers'),
            'q': self.choice_draft_speakers}
        self.choices['published_speakers'] = {
            'label': _('accepted speakers'),
            'q': self.choice_published_speakers}


class SendEmailView(StaffUserMixin, SuccessMessageMixin, FormView):
    template_name = 'devday/sendemail.html'
    form_class = SendEmailForm

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.choices = DevDayEmailRecipients()

    def get(self, request, *args, **kwargs):
        self.get_form()
        return super().get(request, *args, **kwargs)

    def get_form_kwargs(self):
        context = super().get_form_kwargs()
        context['recipients'] = self.choices.get_form_choices()
        return context

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_success_url(self):
        return reverse_lazy('send_email')

    def form_valid(self, form):
        conv = HTML2Text()
        conv.ignore_images = True
        conv.inline_links = False
        conv.use_automatic_links = True
        html_message = form.cleaned_data['body']
        message = conv.handle(html_message)
        msg = DevDayEmailMessage(
            subject=form.cleaned_data['subject'],
            body=message,
            from_email=settings.DEFAULT_EMAIL_SENDER,
            to=(_('Dev Day Attendees {}').format('<undisclosed-recipients:;>'),
                ),
        )
        msg.extra_headers['From'] = _(
            'Dev Day <{}>').format(settings.DEFAULT_FROM_EMAIL)
        msg.attach_alternative(html_message, "text/html")
        recipients = form.cleaned_data['recipients']
        if form.cleaned_data.get('sendreal'):
            msg.recipientlist = self.choices.get_email_addresses(recipients)
            msg.recipientlist += [settings.DEFAULT_FROM_EMAIL]
            self.success_message = _(
                'Successfully sent message to {} {} recipients'
            ).format(
                len(msg.recipientlist),
                self.choices.get_choice_label(recipients))
            msg.send()
            return super().form_valid(form)
        else:
            msg.recipientlist = (self.request.user.email,)
            self.success_message = _(
                'Successfully sent message for {} to yourself'
            ).format(self.choices.get_choice_label(recipients))
            messages.success(self.request, self.success_message)
            msg.send()
            return self.render_to_response(self.get_context_data(form=form))


class StaticPlaceholderView(StaffUserMixin, TemplateView):
    template_name = 'devday/staticplaceholders.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['placeholders'] = [
            'checkin-instructions',
            'checkin-result',
            'create-talk-introtext',
            'gdpr_teaser',
            'register-attendee-introtext',
            'register-intro',
            'register-intro-anonymous',
            'register-intro-introtext-authenticated',
            'register-success',
            'speaker-register',
            'speaker_registered',
            'sponsoring-intro-text',
            'sponsoring-request-thanks',
            'sponsors',
            'submit-session-introtext',
            'talk_submission_closed',
            'talk_submitted',
        ]
        return context

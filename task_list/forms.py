"""Forms for the ``task_list`` app."""
from django import forms
from django.utils.timezone import now

from .models import Task, TaskList


# ======
# Mixins
# ======

class TaskFormMixin(object):
    """Mixin to add common methods to all Task and TaskList forms."""
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(TaskFormMixin, self).__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        instance = super(TaskFormMixin, self).save(*args, **kwargs)
        if hasattr(instance, 'users'):
            user_list = instance.users
        else:
            user_list = instance.assigned_to
        if not self.user in user_list.all():
            user_list.add(self.user)
        return instance


# =====
# Forms
# =====

class TaskCreateForm(TaskFormMixin, forms.ModelForm):
    """ModelForm to create an instance of the ``Task`` model."""
    class Meta:
        model = Task
        fields = ('title',)

    def __init__(self, user, task_list, *args, **kwargs):
        # add optional param ctype_pk
        self.task_list = task_list
        super(TaskCreateForm, self).__init__(user, *args, **kwargs)

    def save(self, *args, **kwargs):
        self.instance.task_list = self.task_list
        instance = super(TaskCreateForm, self).save(*args, **kwargs)
        # if self.ctype, create Parent instance and connect this task list
        # to parent instance
        return instance


class TaskDoneToggleForm(forms.Form):
    """Form to toggle a tasks done status."""
    task = forms.ModelChoiceField(
        queryset=Task.objects.all(),
    )

    def save(self):
        task = self.cleaned_data.get('task')
        if task.is_done:
            task.is_done = None
        else:
            task.is_done = now()
        task.save()
        return task


class TaskListCreateForm(TaskFormMixin, forms.ModelForm):
    """ModelForm to create an instance of the ``TaskList`` model."""
    class Meta:
        model = TaskList
        fields = ('title',)


class TaskListUpdateForm(TaskFormMixin, forms.ModelForm):
    """ModelForm to update an instance of the ``TaskList`` model."""
    class Meta:
        model = TaskList
        fields = ('title', 'users')


class TaskUpdateForm(TaskFormMixin, forms.ModelForm):
    """ModelForm to update an instance of the ``TaskList`` model."""
    class Meta:
        model = Task
        fields = ('title', 'description', 'category', 'priority',
                  'due_date', 'assigned_to')

    def __init__(self, user, task_list, *args, **kwargs):
        self.task_list = task_list
        super(TaskUpdateForm, self).__init__(user, *args, **kwargs)

    def save(self, *args, **kwargs):
        self.instance.task_list = self.task_list
        if 'toggle' in self.data:
            task_toggle = self.data.get('task')
            if task_toggle and not self.instance.is_done:
                self.instance.is_done = now()
            else:
                self.instance.is_done = None
        return super(TaskUpdateForm, self).save(*args, **kwargs)

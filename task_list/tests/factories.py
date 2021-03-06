"""Factories for the models of the ``task_list`` app."""
import factory

from ..models import (
    Category,
    Parent,
    Task,
    TaskAttachment,
    TaskList,
)
from .test_app.models import DummyModel


class DummyModelFactory(factory.Factory):
    """Factory for the ``DummyModel`` model."""
    FACTORY_FOR = DummyModel

    user = factory.SubFactory('django_libs.tests.factories.UserFactory')
    dummy_field = factory.Sequence(lambda n: 'dummy {0}'.format(n))


class CategoryFactory(factory.Factory):
    """Factory for the ``Category`` model."""
    FACTORY_FOR = Category

    title = factory.Sequence(lambda n: 'category{0}'.format(n))


class ParentFactory(factory.Factory):
    """Factory for the ``Parent`` model."""
    FACTORY_FOR = Parent

    content_object = factory.SubFactory(
        'task_list.tests.factories.DummyModelFactory')
    task_list = factory.SubFactory('task_list.tests.factories.TaskListFactory')


class TaskAttachmentFactory(factory.Factory):
    """Factory for the ``TaskAttachment`` model."""
    FACTORY_FOR = TaskAttachment

    task = factory.SubFactory('task_list.tests.factories.TaskFactory')


class TaskListFactory(factory.Factory):
    """Factory for the ``TaskList`` model."""
    FACTORY_FOR = TaskList

    title = factory.Sequence(lambda n: 'list{0}'.format(n))


class TaskFactory(factory.Factory):
    """Factory for the ``Task`` model."""
    FACTORY_FOR = Task

    title = factory.Sequence(lambda n: 'task{0}'.format(n))
    task_list = factory.SubFactory('task_list.tests.factories.TaskListFactory')

# -*- coding: utf-8 -*-
"""Debugging for Celery workflows."""
from __future__ import print_function
from time import sleep
import celery
import celery.result


def freeze(result):
    """Freeze the result to an id."""
    if isinstance(result, celery.result.GroupResult):
        result.save()
    if isinstance(result, celery.result.GroupResult):
        type = 'group'
    else:
        type = 'async'
    return type, result.id


def thaw(frozen):
    """Unfreeze a result from an id."""
    type, id = frozen
    classes = {
        'async': celery.result.AsyncResult,
        'group': celery.result.GroupResult.restore,
    }
    return classes[type](id)


def ready(result):
    """Determine if the tasks from the result are ready.

    This is separate from the _status_ of the combined tasks,
    since tasks may still be running, for instance in groups,
    but we may already know what the status would be.
    """
    if not result:
        return
    if ready(result.parent) and result.parent.status == 'FAILURE':
        return True
    if isinstance(result, celery.result.GroupResult):
        return all(ready(task_result) for task_result in result.results)
    return result and result.ready()


def watch(signature, duration=100, thawed=False):
    """Watch a celery signature for completion.

    Show intermediate statuses while waiting, and compare states
    between the original result, and one that has been frozen and
    thawed, as would be required for serialization and storage.
    """
    original_result = signature.delay()
    thawed_result = thaw(freeze(original_result))

    try:
        print('====== Initial Statuses ======')
        print('Original: {}'.format(display_status(original_result)))
        print('Thawed: {}'.format(display_status(thawed_result)))
        print('====== Incremental Statuses ({}) ======'.format(
            'Thawed' if thawed else 'Original'))
        sleep(1)  # print on odd seconds
        for i in range(1, duration, 2):
            if ready(original_result):
                print('Ready. Original: {} Thawed: {}'.format(
                    READY[ready(original_result)],
                    READY[ready(thawed_result)],
                ))
                break
            print('{}: {}'.format(i, display_status(
                thawed_result if thawed else original_result)))
            sleep(1 if i >= duration else 2)
    except KeyboardInterrupt:
        print('\b', end='')  # Overwrite the ^C

    print('====== Final Status ======')
    print('Original: {}'.format(display_status(original_result)))
    print('Thawed: {}'.format(display_status(thawed_result)))


CODES = {'PENDING': '🕰 ', 'FAILURE': '👎 ', 'SUCCESS': '👍 '}
READY = {True: u'✅ ', False: u'❌ ', None: '🤷 '}


def display_status(result):
    """Display the status of a result.

    Use an abbreviated form to succinctly show us the properties
    and depth-wise structure and state of a result.
    """
    if result is None:
        return '🤷 '

    output = ''
    if isinstance(result, celery.result.GroupResult):
        output += '(' + ' & '.join(
            display_status(result) for result in result.results
        ) + ')' + READY[result.ready()]
    else:
        output += CODES[result.status] + READY[result.ready()]

    if result.parent:  # Part of a chain.
        output = display_status(result.parent) + ' | ' + output

    return output

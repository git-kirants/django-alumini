from celery.signals import task_success, task_failure, task_revoked, task_retry
from django.core.cache import cache
from django.utils import timezone
import logging

logger = logging.getLogger(__name__)

def update_task_metrics(task_id, status, runtime=None):
    """Update task metrics in cache"""
    metrics_key = f'celery_metrics_{timezone.now().date()}'
    metrics = cache.get(metrics_key, {
        'total': 0,
        'success': 0,
        'failure': 0,
        'revoked': 0,
        'retry': 0,
        'avg_runtime': 0,
        'total_runtime': 0
    })
    
    metrics['total'] += 1
    metrics[status] += 1
    
    if runtime:
        metrics['total_runtime'] += runtime
        metrics['avg_runtime'] = metrics['total_runtime'] / metrics['total']
    
    cache.set(metrics_key, metrics, 86400)  # Store for 24 hours

@task_success.connect
def task_success_handler(sender=None, **kwargs):
    task_id = kwargs.get('task_id')
    runtime = kwargs.get('runtime')
    update_task_metrics(task_id, 'success', runtime)
    logger.info(f'Task {task_id} completed successfully in {runtime}s')

@task_failure.connect
def task_failure_handler(sender=None, **kwargs):
    task_id = kwargs.get('task_id')
    exception = kwargs.get('exception')
    update_task_metrics(task_id, 'failure')
    logger.error(f'Task {task_id} failed: {exception}')

@task_revoked.connect
def task_revoked_handler(sender=None, **kwargs):
    task_id = kwargs.get('task_id')
    update_task_metrics(task_id, 'revoked')
    logger.warning(f'Task {task_id} was revoked')

@task_retry.connect
def task_retry_handler(sender=None, **kwargs):
    task_id = kwargs.get('task_id')
    update_task_metrics(task_id, 'retry')
    logger.info(f'Task {task_id} is being retried') 
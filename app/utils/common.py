import logging

logger = logging.getLogger(__name__)


def calculate_matching_score(worker, job):
    matching_score = 0
    is_same_discipline = False

    if worker.discipline == job.discipline:
        is_same_discipline = True
        matching_score += 25

    if is_same_discipline and job.specialty in worker.specialties:
        matching_score += 25

    if job.state in worker.preferred_working_states:
        matching_score += 25

    if worker.avg_weekly_pay_amount <= job.pay_amount:
        matching_score += 25

    return float(matching_score)

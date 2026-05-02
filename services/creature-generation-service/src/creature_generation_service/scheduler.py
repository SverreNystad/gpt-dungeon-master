from src.models import Job


def select_next_jobs(queued_jobs: list[Job]) -> list[Job]:
    
    # Ensure Fairness
    # * A user that sends many requests gets lower priority in queue
    # Ensure no starvation
    

    return [queued_jobs[0]]

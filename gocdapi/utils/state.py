""" Enumerates results and states used by Go CD. """
ASSIGNED = 'Assigned'
BUILDING = 'Building'
CANCELLED = 'Cancelled'
COMPLETED = 'Completed'
COMPLETING = 'Completing'
DISCONTINUED = 'Discontinued'
FAILED = 'Failed'
FAILING = 'Failing'
PASSED = 'Passed'
PAUSED = 'Paused'
PREPARING = 'Preparing'
RESCHEDULED = 'Rescheduled'
SCHEDULED = 'Scheduled'
UNKNOWN = 'Unknown'
WAITING = 'Waiting'


JOB_RESULTS = [
    CANCELLED,
    FAILED,
    PASSED,
    UNKNOWN,
]

JOB_STATES = [
    ASSIGNED,
    BUILDING,
    COMPLETED,
    COMPLETING,
    DISCONTINUED,
    PAUSED,
    PREPARING,
    RESCHEDULED,
    SCHEDULED,
    UNKNOWN,
    WAITING,
]

STAGE_RESULTS = [
    CANCELLED,
    FAILED,
    PASSED,
    UNKNOWN,
]

STAGE_STATES = [
    BUILDING,
    CANCELLED,
    FAILED,
    FAILING,
    PASSED,
    UNKNOWN,
]

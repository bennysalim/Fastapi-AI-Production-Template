from enum import Enum


class TicketStatusEnum(str, Enum):
    submit="SUBMIT"
    checking_process="CHECKING_PROCESS"
    need_payment_process="NEED_PAYMENT_PROCESS"
    paid_and_work_in_progress="PAID_AND_WORK_IN_PROGRESS"
    handle_and_complete="HANDLE_AND_COMPLETE"
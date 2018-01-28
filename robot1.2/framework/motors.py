import ev3dev.ev3 as ev3


class SynchronisedMotor(ev3.Motor):
    SYSTEM_CLASS_NAME = ev3.Motor.SYSTEM_CLASS_NAME
    SYSTEM_DEVICE_NAME_CONVENTION = '*'
    __slots__ = []

    def __init__(
        self,
        motorName,
        synchroniser,
        driver_name,
        address=None,
        name_pattern=SYSTEM_DEVICE_NAME_CONVENTION,
        name_exact=False,
        **kwargs
    ):
        super(SynchronisedMotor, self).__init__(
            address, name_pattern, name_exact, driver_name, **kwargs)

        self._motorName = motorName
        self._sync = synchroniser

    def run_to_abs_pos(self, **kwargs):
        # change kwargs['pos']
        super(kwargs)
        # after the motor stops rewrite the internals of the file

    def run_to_rel_pos(self, **kwargs):
        super(kwargs)

    def run_timed(self, **kwargs):
        super(kwargs)


class LargeMotor(SynchronisedMotor):

    SYSTEM_CLASS_NAME = SynchronisedMotor.SYSTEM_CLASS_NAME
    SYSTEM_DEVICE_NAME_CONVENTION = '*'
    __slots__ = []

    def __init__(
        self,
        motorName,
        synchroniser,
        address=None,
        name_pattern=SYSTEM_DEVICE_NAME_CONVENTION,
        name_exact=False,
        **kwargs
    ):
        super(LargeMotor, self).__init__(
            motorName,
            synchroniser,
            driver_name=['lego-ev3-l-motor', 'lego-nxt-motor'],
            address=address,
            name_pattern=name_pattern,
            name_exact=name_exact,
            **kwargs
        )


class MediumMotor(SynchronisedMotor):

    SYSTEM_CLASS_NAME = SynchronisedMotor.SYSTEM_CLASS_NAME
    SYSTEM_DEVICE_NAME_CONVENTION = '*'
    __slots__ = []

    def __init__(
        self,
        motorName,
        synchroniser,
        address=None,
        name_pattern=SYSTEM_DEVICE_NAME_CONVENTION,
        name_exact=False,
        **kwargs
    ):
        super(MediumMotor, self).__init__(
            motorName,
            synchroniser,
            driver_name=['lego-ev3-m-motor'],
            address=address,
            name_pattern=name_pattern,
            name_exact=name_exact,
            **kwargs
        )

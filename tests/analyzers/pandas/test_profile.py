from recap.analyzers.pandas.profile import ColumnProfile


class TestColumnProfile:
    def test_instance_creation(self):
        column_profile = ColumnProfile(
            count=10,
            unique=5,
            top="A",
            freq=2,
            mean=3.4,
            std=1.0,
            min=1.0,
            p25=1.5,
            p50=3.0,
            p75=4.5,
            p95=5.0,
            p99=5.5,
            p999=6.0,
            max=7.0,
        )
        assert isinstance(column_profile, ColumnProfile)
        assert column_profile.count == 10
        assert column_profile.unique == 5
        assert column_profile.top == "A"
        assert column_profile.freq == 2
        assert column_profile.mean == 3.4
        assert column_profile.std == 1.0
        assert column_profile.min == 1.0
        assert column_profile.p25 == 1.5
        assert column_profile.p50 == 3.0
        assert column_profile.p75 == 4.5
        assert column_profile.p95 == 5.0
        assert column_profile.p99 == 5.5
        assert column_profile.p999 == 6.0
        assert column_profile.max == 7.0

    def test_default_values(self):
        column_profile = ColumnProfile(count=10)
        assert isinstance(column_profile, ColumnProfile)
        assert column_profile.count == 10
        assert column_profile.unique is None
        assert column_profile.top is None
        assert column_profile.freq is None
        assert column_profile.mean is None
        assert column_profile.std is None
        assert column_profile.min is None
        assert column_profile.p25 is None
        assert column_profile.p50 is None
        assert column_profile.p75 is None
        assert column_profile.p95 is None
        assert column_profile.p99 is None
        assert column_profile.p999 is None
        assert column_profile.max is None

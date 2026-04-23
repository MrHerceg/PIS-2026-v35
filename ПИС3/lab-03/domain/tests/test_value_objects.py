import pytest
from domain.value_objects.location import Location
from domain.value_objects.date_range import DateRange
from domain.value_objects.money import Money


# ─────────────────────────── Location ────────────────────────────────────────

class TestLocation:
    def test_valid_location_name_only(self):
        loc = Location("Paris")
        assert loc.name == "Paris"
        assert loc.latitude is None
        assert loc.longitude is None

    def test_valid_location_with_coords(self):
        loc = Location("Paris", latitude=48.8566, longitude=2.3522)
        assert loc.latitude == 48.8566
        assert loc.longitude == 2.3522

    def test_empty_name_raises(self):
        with pytest.raises(ValueError):
            Location("")

    def test_whitespace_name_raises(self):
        with pytest.raises(ValueError):
            Location("   ")

    def test_invalid_latitude_raises(self):
        with pytest.raises(ValueError):
            Location("X", latitude=91.0)

    def test_invalid_latitude_negative_raises(self):
        with pytest.raises(ValueError):
            Location("X", latitude=-91.0)

    def test_invalid_longitude_raises(self):
        with pytest.raises(ValueError):
            Location("X", longitude=181.0)

    def test_immutability(self):
        loc = Location("Paris")
        with pytest.raises(Exception):
            loc.name = "London"

    def test_equality(self):
        loc1 = Location("Paris", 48.8566, 2.3522)
        loc2 = Location("Paris", 48.8566, 2.3522)
        assert loc1 == loc2

    def test_inequality(self):
        loc1 = Location("Paris")
        loc2 = Location("London")
        assert loc1 != loc2


# ─────────────────────────── DateRange ───────────────────────────────────────

class TestDateRange:
    def test_valid_date_range(self):
        dr = DateRange("2026-05-01", "2026-05-10")
        assert dr.duration_days == 9

    def test_same_day_range(self):
        dr = DateRange("2026-05-01", "2026-05-01")
        assert dr.duration_days == 0

    def test_start_after_end_raises(self):
        with pytest.raises(ValueError):
            DateRange("2026-06-05", "2026-06-01")

    def test_immutability(self):
        dr = DateRange("2026-05-01", "2026-05-10")
        with pytest.raises(Exception):
            dr.start_date = "2026-06-01"

    def test_equality(self):
        dr1 = DateRange("2026-05-01", "2026-05-10")
        dr2 = DateRange("2026-05-01", "2026-05-10")
        assert dr1 == dr2


# ─────────────────────────── Money ───────────────────────────────────────────

class TestMoney:
    def test_valid_money(self):
        m = Money(100.0, "USD")
        assert m.amount == 100.0
        assert m.currency == "USD"

    def test_zero_amount_valid(self):
        m = Money(0, "EUR")
        assert m.amount == 0

    def test_negative_amount_raises(self):
        with pytest.raises(ValueError):
            Money(-1, "USD")

    def test_invalid_currency_raises(self):
        with pytest.raises(ValueError):
            Money(100, "US")

    def test_currency_lowercase_normalized(self):
        m = Money(100, "usd")
        assert m.currency == "USD"

    def test_add_same_currency(self):
        result = Money(100, "USD").add(Money(50, "USD"))
        assert result.amount == 150
        assert result.currency == "USD"

    def test_add_different_currency_raises(self):
        with pytest.raises(ValueError):
            Money(100, "USD").add(Money(50, "EUR"))

    def test_subtract(self):
        result = Money(100, "USD").subtract(Money(30, "USD"))
        assert result.amount == 70

    def test_subtract_would_be_negative_raises(self):
        with pytest.raises(ValueError):
            Money(10, "USD").subtract(Money(20, "USD"))

    def test_immutability(self):
        m = Money(100, "USD")
        with pytest.raises(Exception):
            m.amount = 200

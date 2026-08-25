import datetime
import pathlib
import sys
import unittest


PYTHON_DIR = pathlib.Path(__file__).resolve().parents[1] / "python"
sys.path.insert(0, str(PYTHON_DIR))

import lak_jeng  # noqa: E402
import lak_ni  # noqa: E402
import sakkaraj  # noqa: E402


class AhomLakniTests(unittest.TestCase):
    """Anchors from Kapoor 2021, Tables 7-9 and pp. 668, 686-687."""

    def test_canonical_table_positions(self):
        expected = {
            1: "Kap Cheu",
            7: "Khut Shinga",
            18: "Rung Shiu",
            26: "Kat Plao",
            43: "Rai Shinga",
            60: "Ka Keu",
        }
        for position, name in expected.items():
            self.assertEqual(lak_ni.AHOM_LAKNI_60[position - 1], name)

    def test_2008_cycle_table_anchor(self):
        result = lak_ni.ahom_lakni_for_cycle_year(2008)
        self.assertEqual((result["position"], result["name"]), (1, "Kap Cheu"))
        self.assertIsNone(result["boundary_model"])

    def test_reconstructed_new_year_has_priority_over_old_month(self):
        boundary = lak_ni.ahom_dinching_start_jdn(2025)
        self.assertEqual(lak_ni.jdn_to_date(boundary), datetime.date(2025, 11, 21))
        before = lak_ni.ahom_calendar_for_date(2025, 11, 20)
        after = lak_ni.ahom_calendar_for_date(2025, 11, 21)
        self.assertEqual((before["cycle_year"], after["cycle_year"]), (2024, 2025))
        self.assertEqual((after["position"], after["name"]), (18, "Rung Shiu"))
        self.assertEqual((after["month_number"], after["month_name"],
                          after["month_day"]), (1, "Din Ching", 1))
        self.assertEqual(after["preceding_new_moon_date"], datetime.date(2025, 11, 20))
        self.assertEqual(after["new_year_change_local"].hour, 0)
        self.assertEqual(after["boundary_priority"],
                         "change Lakni and start Din Ching day 1 together")

    def test_reconstructed_leap_lunation_follows_month_eight(self):
        result = lak_ni.ahom_calendar_for_date(2024, 11, 2)
        self.assertEqual(result["months_in_year"], 13)
        starts = lak_ni.ahom_month_starts(2024)
        leap_date = lak_ni.jdn_to_date(starts[8])
        leap = lak_ni.ahom_calendar_for_date(
            leap_date.year, leap_date.month, leap_date.day)
        self.assertTrue(leap["is_leap_month"])
        self.assertEqual((leap["month_number"], leap["month_name"],
                          leap["month_day"]), (8, "Leap after Din Pet", 1))

    def test_report_labels_reconstruction_and_separates_nadaw(self):
        report = lak_ni.full_report(2026, 8, 23)
        self.assertIn("Ahom Lakni*", report)
        self.assertIn("Ahom month*", report)
        self.assertIn("Ganzhi compare : Rai-Singa", report)
        self.assertIn("not a Nadaw conversion", report)
        self.assertNotIn("folk Me-Pi", report)


class MyanmarCalendarTests(unittest.TestCase):
    """Regression anchors from Yan Naing Aye's MIT-licensed mmcal implementation."""

    def test_exception_years(self):
        expected = {
            1263: "big watat",
            1264: "common",
            1344: "little watat",
            1345: "common",
            1377: "big watat",
        }
        for year, prefix in expected.items():
            self.assertTrue(sakkaraj.watat_type(year)["type"].startswith(prefix))

    def test_published_second_waso_anchors(self):
        self.assertEqual(sakkaraj.watat_type(1374)["waso_fm"], 2456142)
        self.assertEqual(sakkaraj.watat_type(1377)["waso_fm"], 2457235)
        self.assertEqual(sakkaraj.jdn_to_gregorian(2457235), datetime.date(2015, 7, 31))

    def test_myanmar_round_trips_across_eras(self):
        samples = [
            (205, 4, 15),
            (813, 9, 1),
            (1120, 4, 15),
            (1263, 0, 1),
            (1344, 9, 1),
            (1387, 9, 1),
        ]
        for my, month, day in samples:
            jdn = sakkaraj.myanmar_to_jdn(my, month, day)
            converted = sakkaraj.jdn_to_myanmar(jdn)
            self.assertEqual((converted["my"], converted["month"], converted["month_day"]),
                             (my, month, day))

    def test_dynamic_solar_new_year_boundary(self):
        self.assertEqual(sakkaraj.cs_year_for(2015, 4, 16), 1376)
        self.assertEqual(sakkaraj.cs_year_for(2015, 4, 17), 1377)

    def test_thai_avoman_uses_canonical_692_for_zero_remainder(self):
        self.assertEqual(sakkaraj.thai_new_year_integers(856)["avoman"], 692)


class LakJengTests(unittest.TestCase):
    def test_shan_year_2120_boundary(self):
        self.assertEqual(lak_jeng.tai_new_year_jdn(2025), lak_jeng.to_jdn(2025, 11, 20))
        self.assertEqual(lak_jeng.tai_year_from_gregorian(2025, 11, 19), 2119)
        self.assertEqual(lak_jeng.tai_year_from_gregorian(2025, 11, 20), 2120)

    def test_tai_month_one_is_nadaw_waxing_one(self):
        result = sakkaraj.tai_lunar_new_year(2025)
        self.assertEqual(result["gregorian_date"], datetime.date(2025, 11, 20))
        self.assertEqual((result["tai_month"], result["tai_phase"],
                          result["tai_fortnight_day"]), (1, "waxing", 1))
        self.assertEqual(result["myanmar_month_name"], "Nadaw")

    def test_source_discrepancy_remains_explicit(self):
        self.assertEqual(lak_jeng.calculate(2116)["a"], 772531)
        self.assertEqual(lak_jeng.a_for_date(2021, 12, 5), 772521)
        self.assertEqual(lak_jeng.calculate(2116)["a"] -
                         lak_jeng.a_for_date(2021, 12, 5), 10)

    def test_market_day_label_matches_indices(self):
        for offset in range(10):
            dt = datetime.date(2026, 8, 23) + datetime.timedelta(days=offset)
            report = lak_jeng.report_date(dt.year, dt.month, dt.day)
            idx = lak_jeng.day_index_from_a(lak_jeng.a_for_date(dt.year, dt.month, dt.day))
            self.assertEqual("market day      : yes" in report, idx % 10 in (2, 7))


if __name__ == "__main__":
    unittest.main()

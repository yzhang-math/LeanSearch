--@funsearch.evolve
theorem mathd_algebra_101 (x : ℝ) (h₀ : x ^ 2 - 5 * x - 4 ≤ 10) : x ≥ -2 ∧ x ≤ 7 := by
  simp_all only [rpow_two, tsub_le_iff_right, ge_iff_le]
  apply And.intro
  · nlinarith
  · nlinarith

--@funsearch.run
theorem irrelevant : 2 + 3 = 3 + 2 := by
   sorry

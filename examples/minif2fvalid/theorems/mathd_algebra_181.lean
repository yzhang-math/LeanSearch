--@funsearch.evolve
theorem mathd_algebra_181 (n : ℝ) (h₀ : n ≠ 3) (h₁ : (n + 5) / (n - 3) = 2) : n = 11 := by
  rw [div_eq_iff] at h₁
  linarith
  exact sub_ne_zero.mpr h₀

--@funsearch.run
theorem irrelevant : 2 + 3 = 3 + 2 := by
   sorry

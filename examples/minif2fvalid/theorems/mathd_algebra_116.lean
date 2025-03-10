--@funsearch.evolve
theorem mathd_algebra_116 (k x : ℝ) (h₀ : x = (13 - Real.sqrt 131) / 4)
    (h₁ : 2 * x ^ 2 - 13 * x + k = 0) : k = 19 / 4 := by
  rw [h₀] at h₁
  rw [eq_comm.mp (add_eq_zero_iff_neg_eq.mp h₁)]
  norm_num
  rw [pow_two]
  sorry

--@funsearch.run
theorem irrelevant : 2 + 3 = 3 + 2 := by
   sorry

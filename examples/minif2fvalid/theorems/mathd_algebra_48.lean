--@funsearch.evolve
theorem mathd_algebra_48 (q e : ℂ) (h₀ : q = 9 - 4 * Complex.I) (h₁ : e = -3 - 4 * Complex.I) :
  q - e = 12 := by
  subst h₁ h₀
  simp_all only [sub_sub_sub_cancel_right, sub_neg_eq_add]
  norm_num

--@funsearch.run
theorem irrelevant : 2 + 3 = 3 + 2 := by
   sorry

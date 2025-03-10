--@funsearch.evolve
theorem mathd_algebra_51 (a b : ℝ) (h₀ : 0 < a ∧ 0 < b) (h₁ : a + b = 35) (h₂ : a = 2 / 5 * b) :
    b - a = 15 := by
  subst h₂
  simp_all only [ofNat_pos, div_pos_iff_of_pos_left, mul_pos_iff_of_pos_left, and_self]
  linarith

--@funsearch.run
theorem irrelevant : 2 + 3 = 3 + 2 := by
   sorry

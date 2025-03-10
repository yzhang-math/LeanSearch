--@funsearch.evolve
theorem mathd_algebra_327 (a : ℝ) (h₀ : 1 / 5 * abs (9 + 2 * a) < 1) : -7 < a ∧ a < -2 := by
  have h₁ := (mul_lt_mul_left (show 0 < (5 : ℝ) by linarith)).mpr h₀
  have h₂ : abs (9 + 2 * a) < 5 := by linarith
  have h₃ := abs_lt.mp h₂
  cases' h₃ with h₃ h₄
  constructor <;> nlinarith

--@funsearch.run
theorem irrelevant : 2 + 3 = 3 + 2 := by
   sorry

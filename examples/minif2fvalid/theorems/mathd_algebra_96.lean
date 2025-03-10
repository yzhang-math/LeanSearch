--@funsearch.evolve
theorem mathd_algebra_96 (x y z a : ℝ) (h₀ : 0 < x ∧ 0 < y ∧ 0 < z)
  (h₁ : Real.log x - Real.log y = a) (h₂ : Real.log y - Real.log z = 15)
  (h₃ : Real.log z - Real.log x = -7) : a = -8 := by
  subst h₁
  obtain ⟨left, right⟩ := h₀
  obtain ⟨left_1, right⟩ := right
  linarith

--@funsearch.run
theorem irrelevant : 2 + 3 = 3 + 2 := by
   sorry

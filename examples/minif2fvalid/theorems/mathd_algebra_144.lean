--@funsearch.evolve
theorem mathd_algebra_144 (a b c d : ℕ) (h₀ : 0 < a ∧ 0 < b ∧ 0 < c ∧ 0 < d) (h₀ : (c : ℤ) - b = d)
    (h₁ : (b : ℤ) - a = d) (h₂ : a + b + c = 60) (h₃ : a + b > c) : d < 10 := by
  rename_i h₀_1
  simp_all only [gt_iff_lt]
  obtain ⟨left, right⟩ := h₀_1
  obtain ⟨left_1, right⟩ := right
  obtain ⟨left_2, right⟩ := right
  linarith

--@funsearch.run
theorem irrelevant : 2 + 3 = 3 + 2 := by
   sorry

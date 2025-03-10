--@funsearch.evolve
theorem amc12_2000_p11 (a b : ℝ) (h₀ : a ≠ 0 ∧ b ≠ 0) (h₁ : a * b = a - b) :
    a / b + b / a - a * b = 2 := by
  field_simp [h₀.1, h₀.2]
  simp only [h₁, mul_comm, mul_sub]
  ring

--@funsearch.run
theorem irrelevant : 2 + 3 = 3 + 2 := by
   sorry

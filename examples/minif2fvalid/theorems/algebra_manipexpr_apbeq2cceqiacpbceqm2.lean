--@funsearch.evolve
theorem algebra_manipexpr_apbeq2cceqiacpbceqm2 (a b c : ℂ) (h₀ : a + b = 2 * c)
  (h₁ : c = Complex.I) : a * c + b * c = -2 := by
  rw [← add_mul, h₀, h₁, mul_assoc, Complex.I_mul_I]
  ring

--@funsearch.run
theorem irrelevant : 2 + 3 = 3 + 2 := by
   sorry

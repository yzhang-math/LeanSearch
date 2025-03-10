--@funsearch.evolve
theorem amc12a_2021_p25
  (N : ℕ)
  (f : ℕ → ℝ)
  (h₀ : ∀ n, 0 < n → f n = ((Nat.divisors n).card)/(n^((1:ℝ)/3)))
  (h₁ : ∀ n ≠ N, 0 < n → f n < f N) :
  (Nat.digits 10 N).sum = 9 := by sorry

--@funsearch.run
theorem irrelevant : 2 + 3 = 3 + 2 := by
   sorry

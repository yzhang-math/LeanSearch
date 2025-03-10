--@funsearch.evolve
theorem imo_1978_p5 (n : ℕ) (a : ℕ → ℕ) (h₀ : Function.Injective a) (h₁ : a 0 = 0) (h₂ : 0 < n) :
  (∑ k in Finset.Icc 1 n, (1 : ℝ) / k) ≤ ∑ k in Finset.Icc 1 n, (a k : ℝ) / k ^ 2 := by
  sorry

--@funsearch.run
theorem irrelevant : 2 + 3 = 3 + 2 := by
   sorry

--@funsearch.evolve
theorem mathd_numbertheory_451
  (S : Finset ℕ)
  (h₀ : ∀ (n : ℕ), n ∈ S ↔ 2010 ≤ n ∧ n ≤ 2019 ∧ ∃ m, ((Nat.divisors m).card = 4 ∧ ∑ p in (Nat.divisors m), p = n)) :
  ∑ k in S, k = 2016 := by sorry

--@funsearch.run
theorem irrelevant : 2 + 3 = 3 + 2 := by
   sorry

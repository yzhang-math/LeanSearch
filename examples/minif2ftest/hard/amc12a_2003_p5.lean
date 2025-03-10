--@funsearch.evolve
theorem amc12a_2003_p5
  (A M C : ℕ)
  (h₀ : A ≤ 9 ∧ M ≤ 9 ∧ C ≤ 9)
  (h₁ : Nat.ofDigits 10 [0,1,C,M,A] + Nat.ofDigits 10 [2,1,C,M,A] = 123422) :
  A + M + C = 14 := by sorry

--@funsearch.run
theorem irrelevant : 2 + 3 = 3 + 2 := by
   sorry

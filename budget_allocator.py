#!/usr/bin/env python3
"""
Flexible Budget & Investment Allocator
=======================================
A command-line personal finance tool that helps users track income,
manage expenses, build emergency funds, and allocate investments.
"""

import csv
import os
from datetime import datetime


# ──────────────────────────────────────────────
# Input Helpers
# ──────────────────────────────────────────────

def get_float_input(prompt: str, *, allow_zero: bool = True) -> float:
    """Safely prompt the user for a non-negative numeric value.

    Args:
        prompt: The message displayed to the user.
        allow_zero: Whether zero is accepted as valid input.

    Returns:
        A validated non-negative float.
    """
    while True:
        raw = input(prompt).strip()
        try:
            value = float(raw)
        except ValueError:
            print("  ⚠  Please enter a valid number.")
            continue

        if value < 0:
            print("  ⚠  Value cannot be negative.")
            continue

        if not allow_zero and value == 0:
            print("  ⚠  Value must be greater than zero.")
            continue

        return value


def get_int_input(prompt: str, low: int = 1, high: int = 12) -> int:
    """Prompt the user for an integer within a given range.

    Args:
        prompt: The message displayed to the user.
        low: Minimum accepted value (inclusive).
        high: Maximum accepted value (inclusive).

    Returns:
        A validated integer in [low, high].
    """
    while True:
        raw = input(prompt).strip()
        try:
            value = int(raw)
        except ValueError:
            print(f"  ⚠  Please enter a whole number between {low} and {high}.")
            continue

        if low <= value <= high:
            return value
        print(f"  ⚠  Please enter a number between {low} and {high}.")


def get_yes_no(prompt: str) -> bool:
    """Prompt the user for a yes/no answer.

    Returns:
        True for yes, False for no.
    """
    while True:
        raw = input(prompt).strip().lower()
        if raw in ("y", "yes"):
            return True
        if raw in ("n", "no"):
            return False
        print("  ⚠  Please enter 'y' or 'n'.")


# ──────────────────────────────────────────────
# Data Collection
# ──────────────────────────────────────────────

def collect_income() -> float:
    """Collect total monthly income from the user.

    Returns:
        Total monthly income as a float.
    """
    print("\n╔══════════════════════════════════════╗")
    print("║        💰  MONTHLY INCOME            ║")
    print("╚══════════════════════════════════════╝")
    return get_float_input("  Enter your total monthly income: $", allow_zero=False)


def collect_essential_expenses() -> dict[str, float]:
    """Collect fixed essential monthly expenses.

    Returns:
        A dictionary mapping expense names to their amounts.
    """
    print("\n╔══════════════════════════════════════╗")
    print("║     🏠  ESSENTIAL EXPENSES           ║")
    print("╚══════════════════════════════════════╝")
    print("  (Rent, utilities, insurance, loan payments, etc.)\n")

    essentials: dict[str, float] = {}
    categories = [
        ("Rent / Mortgage", "rent_mortgage"),
        ("Utilities (electric, water, internet)", "utilities"),
        ("Insurance (health, car, etc.)", "insurance"),
        ("Loan / Debt Payments", "loan_payments"),
        ("Groceries", "groceries"),
        ("Transportation", "transportation"),
    ]

    for display_name, _key in categories:
        amount = get_float_input(f"  {display_name}: $")
        if amount > 0:
            essentials[display_name] = amount

    # Allow custom essential expenses
    while get_yes_no("\n  Add another essential expense? (y/n): "):
        name = input("    Expense name: ").strip()
        if not name:
            print("  ⚠  Name cannot be empty.")
            continue
        amount = get_float_input(f"    {name}: $")
        if amount > 0:
            essentials[name] = amount

    return essentials


def collect_lifestyle_expenses() -> dict[str, float]:
    """Interactively collect variable lifestyle (non-essential) expenses.

    Returns:
        A dictionary mapping expense names to their amounts.
    """
    print("\n╔══════════════════════════════════════╗")
    print("║     🎯  LIFESTYLE EXPENSES           ║")
    print("╚══════════════════════════════════════╝")
    print("  (Dining out, subscriptions, hobbies, etc.)\n")

    lifestyle: dict[str, float] = {}
    suggestions = [
        "Dining Out / Takeout",
        "Subscriptions (Netflix, Spotify, etc.)",
        "Hobbies / Entertainment",
        "Clothing / Shopping",
        "Personal Care",
    ]

    for name in suggestions:
        amount = get_float_input(f"  {name}: $")
        if amount > 0:
            lifestyle[name] = amount

    while get_yes_no("\n  Add another lifestyle expense? (y/n): "):
        name = input("    Expense name: ").strip()
        if not name:
            print("  ⚠  Name cannot be empty.")
            continue
        amount = get_float_input(f"    {name}: $")
        if amount > 0:
            lifestyle[name] = amount

    return lifestyle


# ──────────────────────────────────────────────
# Calculations (Pure Functions)
# ──────────────────────────────────────────────

def calculate_emergency_fund_target(
    monthly_essentials: float,
    months_coverage: int = 6,
) -> float:
    """Compute the total emergency fund target.

    Args:
        monthly_essentials: Total essential expenses per month.
        months_coverage: Number of months the fund should cover.

    Returns:
        The target emergency fund amount.
    """
    return monthly_essentials * months_coverage


def calculate_emergency_contribution(
    surplus: float,
    emergency_fund_target: float,
    current_savings: float,
    contribution_rate: float = 0.20,
) -> float:
    """Determine how much of the surplus goes to the emergency fund.

    If the fund is already fully funded, returns 0.

    Args:
        surplus: Money remaining after all expenses.
        emergency_fund_target: Desired emergency fund total.
        current_savings: Amount already saved.
        contribution_rate: Fraction of surplus to allocate (default 20 %).

    Returns:
        The dollar amount to contribute this month.
    """
    if current_savings >= emergency_fund_target:
        return 0.0

    remaining_need = emergency_fund_target - current_savings
    ideal_contribution = surplus * contribution_rate
    return min(ideal_contribution, remaining_need, surplus)


def allocate_budget(
    income: float,
    essential_total: float,
    lifestyle_total: float,
) -> dict[str, float]:
    """Distribute income across spending categories and compute surplus.

    Args:
        income: Total monthly income.
        essential_total: Sum of essential expenses.
        lifestyle_total: Sum of lifestyle expenses.

    Returns:
        A dict with keys 'essentials', 'lifestyle', 'total_expenses', 'surplus'.
    """
    total_expenses = essential_total + lifestyle_total
    surplus = income - total_expenses
    return {
        "essentials": essential_total,
        "lifestyle": lifestyle_total,
        "total_expenses": total_expenses,
        "surplus": surplus,
    }


def allocate_investments(
    investable_amount: float,
    allocations: dict[str, float] | None = None,
) -> dict[str, float]:
    """Split investable surplus across asset classes.

    Args:
        investable_amount: Dollars available for investing.
        allocations: A dict mapping asset names to percentage weights
                     (values should sum to 1.0). Defaults to a
                     balanced starter portfolio.

    Returns:
        A dict mapping asset class names to dollar amounts.
    """
    if allocations is None:
        allocations = {
            "Index Funds (e.g. S&P 500 ETF)": 0.40,
            "Bond Funds / Fixed Income": 0.20,
            "International / Emerging Markets": 0.15,
            "REITs (Real Estate)": 0.10,
            "Individual Stocks / Growth": 0.10,
            "Crypto / Speculative": 0.05,
        }

    return {
        name: round(investable_amount * weight, 2)
        for name, weight in allocations.items()
    }


# ──────────────────────────────────────────────
# Reporting
# ──────────────────────────────────────────────

def build_report(
    income: float,
    essentials: dict[str, float],
    lifestyle: dict[str, float],
    budget: dict[str, float],
    emergency_fund_target: float,
    emergency_contribution: float,
    current_savings: float,
    investments: dict[str, float],
) -> str:
    """Build a formatted plain-text budget report.

    Returns:
        The full report as a string.
    """
    lines: list[str] = []
    divider = "═" * 52
    thin = "─" * 52
    now = datetime.now().strftime("%B %Y")

    lines.append("")
    lines.append(f"  ╔{divider}╗")
    lines.append(f"  ║  📊  BUDGET & INVESTMENT REPORT — {now:<16} ║")
    lines.append(f"  ╚{divider}╝")

    # Income
    lines.append(f"\n  💰 Monthly Income:              ${income:>12,.2f}")
    lines.append(f"  {thin}")

    # Essential expenses
    lines.append("\n  🏠 ESSENTIAL EXPENSES:")
    for name, amount in essentials.items():
        lines.append(f"     {name:<35} ${amount:>10,.2f}")
    lines.append(f"     {'SUBTOTAL':<35} ${budget['essentials']:>10,.2f}")

    # Lifestyle expenses
    lines.append("\n  🎯 LIFESTYLE EXPENSES:")
    for name, amount in lifestyle.items():
        lines.append(f"     {name:<35} ${amount:>10,.2f}")
    lines.append(f"     {'SUBTOTAL':<35} ${budget['lifestyle']:>10,.2f}")

    lines.append(f"\n  {thin}")
    lines.append(f"  📋 Total Expenses:              ${budget['total_expenses']:>12,.2f}")
    lines.append(f"  💵 Surplus (before savings):     ${budget['surplus']:>12,.2f}")

    # Emergency fund
    lines.append(f"\n  {thin}")
    lines.append("  🛡️  EMERGENCY FUND:")
    lines.append(f"     Target ({emergency_fund_target / max(budget['essentials'], 1):.0f} months of essentials):"
                 f"       ${emergency_fund_target:>10,.2f}")
    lines.append(f"     Currently Saved:                  ${current_savings:>10,.2f}")
    lines.append(f"     This Month's Contribution:        ${emergency_contribution:>10,.2f}")

    progress = min(
        (current_savings + emergency_contribution) / max(emergency_fund_target, 1) * 100,
        100,
    )
    bar_length = 20
    filled = int(bar_length * progress / 100)
    bar = "█" * filled + "░" * (bar_length - filled)
    lines.append(f"     Progress: [{bar}] {progress:.1f}%")

    # Investments
    investable = budget["surplus"] - emergency_contribution
    lines.append(f"\n  {thin}")
    lines.append("  📈 INVESTMENT ALLOCATION:")
    lines.append(f"     Investable Amount:                ${investable:>10,.2f}")
    if investable > 0:
        for name, amount in investments.items():
            lines.append(f"     {name:<35} ${amount:>10,.2f}")
    else:
        lines.append("     ⚠  No funds available for investing this month.")

    # Summary
    lines.append(f"\n  {thin}")
    savings_rate = (
        (budget["surplus"] / income * 100) if income > 0 else 0
    )
    lines.append(f"  📊 Savings Rate:                 {savings_rate:>11.1f}%")

    if savings_rate >= 20:
        lines.append("  ✅ Great job! You're saving 20 %+ of your income.")
    elif savings_rate >= 10:
        lines.append("  👍 Solid start — aim for 20 % or more over time.")
    elif savings_rate > 0:
        lines.append("  ⚠  Consider reducing lifestyle spending to save more.")
    else:
        lines.append("  🚨 You're spending more than you earn! Review your expenses.")

    lines.append("")
    return "\n".join(lines)


def print_report(report: str) -> None:
    """Display the budget report in the terminal.

    Args:
        report: Pre-formatted report string.
    """
    print(report)


def export_report(
    report: str,
    income: float,
    essentials: dict[str, float],
    lifestyle: dict[str, float],
    budget: dict[str, float],
    emergency_contribution: float,
    investments: dict[str, float],
) -> None:
    """Write the report to both a .txt and a .csv file.

    Files are saved under the ``reports/`` directory relative to this script.

    Args:
        report: Pre-formatted plain-text report.
        income: Monthly income.
        essentials: Essential expense breakdown.
        lifestyle: Lifestyle expense breakdown.
        budget: Budget summary dict.
        emergency_contribution: Emergency fund contribution.
        investments: Investment allocation breakdown.
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    reports_dir = os.path.join(script_dir, "reports")
    os.makedirs(reports_dir, exist_ok=True)

    txt_path = os.path.join(reports_dir, "report.txt")
    csv_path = os.path.join(reports_dir, "report.csv")

    # ── Plain-text export ──
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(report)
    print(f"\n  📄 Report saved to: {txt_path}")

    # ── CSV export ──
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Category", "Item", "Amount"])
        writer.writerow(["Income", "Total Monthly Income", f"{income:.2f}"])

        for name, amount in essentials.items():
            writer.writerow(["Essential Expense", name, f"{amount:.2f}"])

        for name, amount in lifestyle.items():
            writer.writerow(["Lifestyle Expense", name, f"{amount:.2f}"])

        writer.writerow(["Summary", "Total Expenses", f"{budget['total_expenses']:.2f}"])
        writer.writerow(["Summary", "Surplus", f"{budget['surplus']:.2f}"])
        writer.writerow(["Savings", "Emergency Fund Contribution", f"{emergency_contribution:.2f}"])

        for name, amount in investments.items():
            writer.writerow(["Investment", name, f"{amount:.2f}"])

    print(f"  📄 CSV saved to:    {csv_path}")


# ──────────────────────────────────────────────
# Main Workflow
# ──────────────────────────────────────────────

def main() -> None:
    """Entry point: orchestrate the full budget & investment workflow."""
    print("\n" + "=" * 56)
    print("   💸  FLEXIBLE BUDGET & INVESTMENT ALLOCATOR  💸")
    print("=" * 56)

    # 1. Collect data
    income = collect_income()
    essentials = collect_essential_expenses()
    lifestyle = collect_lifestyle_expenses()

    essential_total = sum(essentials.values())
    lifestyle_total = sum(lifestyle.values())

    # 2. Allocate budget
    budget = allocate_budget(income, essential_total, lifestyle_total)

    if budget["surplus"] <= 0:
        print("\n  🚨  Your expenses exceed your income!")
        print("      Please review your spending before investing.\n")

    # 3. Emergency fund
    print("\n╔══════════════════════════════════════╗")
    print("║     🛡️   EMERGENCY FUND              ║")
    print("╚══════════════════════════════════════╝")

    months = get_int_input(
        "  How many months of essentials should your fund cover? (3–12): ",
        low=3,
        high=12,
    )
    emergency_fund_target = calculate_emergency_fund_target(essential_total, months)

    current_savings = get_float_input(
        "  How much do you currently have saved for emergencies? $"
    )

    emergency_contribution = calculate_emergency_contribution(
        surplus=max(budget["surplus"], 0),
        emergency_fund_target=emergency_fund_target,
        current_savings=current_savings,
    )

    # 4. Investment allocation
    investable = max(budget["surplus"] - emergency_contribution, 0)
    investments = allocate_investments(investable)

    # 5. Report
    report = build_report(
        income=income,
        essentials=essentials,
        lifestyle=lifestyle,
        budget=budget,
        emergency_fund_target=emergency_fund_target,
        emergency_contribution=emergency_contribution,
        current_savings=current_savings,
        investments=investments,
    )

    print_report(report)

    # 6. Export
    if get_yes_no("  Would you like to export this report? (y/n): "):
        export_report(
            report=report,
            income=income,
            essentials=essentials,
            lifestyle=lifestyle,
            budget=budget,
            emergency_contribution=emergency_contribution,
            investments=investments,
        )

    print("\n  ✅  All done — happy budgeting! 🎉\n")


if __name__ == "__main__":
    main()

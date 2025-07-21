// NAYAG EDGE - Custom Loan Management
// Main JavaScript file for custom loan functionality

frappe.ready(function() {
    console.log("NAYAG EDGE Custom Loan Management loaded");
    
    // Custom loan calculator functionality
    if (window.location.pathname.includes('loan')) {
        // Add any custom JS functionality here
    }
});

// Loan calculation utilities
window.loan_calculator = {
    calculate_flat_interest: function(principal, rate, tenure) {
        const total_interest = principal * (rate / 100) * tenure;
        const total_amount = principal + total_interest;
        const monthly_payment = total_amount / tenure;
        
        return {
            principal: principal,
            total_interest: total_interest,
            total_amount: total_amount,
            monthly_payment: monthly_payment
        };
    },
    
    calculate_emi: function(principal, rate, tenure) {
        const monthly_rate = rate / 100;
        let emi;
        
        if (monthly_rate === 0) {
            emi = principal / tenure;
        } else {
            emi = (principal * monthly_rate * Math.pow(1 + monthly_rate, tenure)) / 
                  (Math.pow(1 + monthly_rate, tenure) - 1);
        }
        
        const total_amount = emi * tenure;
        const total_interest = total_amount - principal;
        
        return {
            principal: principal,
            emi: emi,
            total_amount: total_amount,
            total_interest: total_interest
        };
    }
};

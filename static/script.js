// jQuery for form validation and UI effects

$(document).ready(function() {
    
    // Form validation for adding habits
    $('#habitForm').on('submit', function(e) {
        let isValid = true;
        
        // Validate habit name
        const habitName = $('#habit_name').val().trim();
        if (habitName === '') {
            e.preventDefault();
            $('#habit_name').addClass('is-invalid');
            isValid = false;
        } else {
            $('#habit_name').removeClass('is-invalid');
        }
        
        // Validate weekly goal
        const weeklyGoal = parseInt($('#weekly_goal').val());
        if (isNaN(weeklyGoal) || weeklyGoal < 1 || weeklyGoal > 7) {
            e.preventDefault();
            $('#weekly_goal').addClass('is-invalid');
            isValid = false;
        } else {
            $('#weekly_goal').removeClass('is-invalid');
        }
        
        // Show success message if valid
        if (isValid) {
            showToast('Habit added successfully! 🎉');
        }
    });
    
    // Remove invalid class on input
    $('#habit_name, #weekly_goal').on('input', function() {
        $(this).removeClass('is-invalid');
    });
    
    // Animate progress bars on page load
    $('.progress-bar').each(function() {
        const width = $(this).css('width');
        $(this).css('width', '0');
        $(this).animate({ width: width }, 1000);
    });
    
    // Confirm button click animation
    $('.mark-complete-btn').on('click', function() {
        $(this).html('✓ Logging...').prop('disabled', true);
    });
    
    // Smooth scroll to top
    $('a[href="/"]').on('click', function(e) {
        if (this.hash !== '') {
            $('html, body').animate({
                scrollTop: 0
            }, 500);
        }
    });
    
    // Toast notification function
    function showToast(message) {
        // Create toast element
        const toast = $('<div class="toast-notification"></div>').text(message);
        $('body').append(toast);
        
        // Add CSS for toast
        toast.css({
            position: 'fixed',
            top: '20px',
            right: '20px',
            background: '#28a745',
            color: 'white',
            padding: '15px 20px',
            borderRadius: '10px',
            boxShadow: '0 5px 15px rgba(0,0,0,0.3)',
            zIndex: 9999,
            animation: 'slideIn 0.3s ease'
        });
        
        // Remove after 3 seconds
        setTimeout(function() {
            toast.fadeOut(500, function() {
                $(this).remove();
            });
        }, 3000);
    }
    
    // Add CSS animation for toast
    $('<style>')
        .text('@keyframes slideIn { from { transform: translateX(400px); opacity: 0; } to { transform: translateX(0); opacity: 1; } }')
        .appendTo('head');
    
    // Hover effect on habit cards
    $('.habit-card').hover(
        function() {
            $(this).addClass('shadow-lg');
        },
        function() {
            $(this).removeClass('shadow-lg');
        }
    );
    
    // Real-time validation feedback
    $('#habit_name').on('blur', function() {
        const value = $(this).val().trim();
        if (value.length < 3) {
            $(this).addClass('is-invalid');
            $(this).siblings('.invalid-feedback').text('Habit name must be at least 3 characters.');
        } else {
            $(this).removeClass('is-invalid');
        }
    });
    
    $('#weekly_goal').on('blur', function() {
        const value = parseInt($(this).val());
        if (isNaN(value) || value < 1 || value > 7) {
            $(this).addClass('is-invalid');
        } else {
            $(this).removeClass('is-invalid');
        }
    });
});

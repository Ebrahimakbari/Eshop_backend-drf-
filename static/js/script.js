$(document).ready(function() {
    const productId = $('#product-id').val();
    const commentsContainer = $('#comments-container');

    // Load Comments Dynamically
    function loadComments() {
        $.ajax({
            url: `/products/${productId}/comments/`,
            method: 'GET',
            success: function(response) {
                commentsContainer.empty();
                renderComments(response);
            },
            error: function() {
                commentsContainer.html('<p>خطا در بارگذاری کامنت‌ها</p>');
            }
        });
    }

    // Recursive Comment Rendering
    function renderComments(comments, parentElement = commentsContainer) {
        comments.forEach(function(comment) {
            const commentElement = createCommentElement(comment);
            parentElement.append(commentElement);

            // Render replies recursively
            if (comment.replies && comment.replies.length > 0) {
                const repliesContainer = commentElement.find('.replies-container');
                renderComments(comment.replies, repliesContainer);
            }
        });
    }

    // Create Comment Element
    function createCommentElement(comment) {
        const commentHtml = `
            <div class="comment" data-comment-id="${comment.id}">
                <div class="comment-content">
                    <p>${comment.text}</p>
                    <div class="comment-meta">
                        <span class="comment-author">${comment.user}</span>
                        <span class="comment-date">${comment.created_date}</span>
                    </div>
                    <button class="btn-reply" data-parent-id="${comment.id}">پاسخ</button>
                </div>
                <div class="replies-container"></div>
            </div>
        `;
        return $(commentHtml);
    }

    // Add Comment Dynamically
    $('#comment-form').on('submit', function(e) {
        e.preventDefault();
        const commentText = $('#comment-text');
        const parentId = $('#parent-id');

        $.ajax({
            url: `/products/${productId}/add-comment/`,
            method: 'POST',
            data: {
                text: commentText.val(),
                parent_id: parentId.val() || null,
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
            },
            success: function(newComment) {
                if (parentId.val()) {
                    // If it's a reply, find the parent and append to its replies
                    const parentComment = $(`.comment[data-comment-id="${parentId.val()}"]`);
                    const repliesContainer = parentComment.find('.replies-container');
                    
                    const newCommentElement = createCommentElement(newComment);
                    repliesContainer.append(newCommentElement);
                } else {
                    // If it's a top-level comment, prepend to main container
                    const newCommentElement = createCommentElement(newComment);
                    commentsContainer.prepend(newCommentElement);
                }

                commentText.val('');
                parentId.val('');
            },
            error: function(xhr) {
                alert(xhr.responseJSON.error || 'خطا در ارسال کامنت');
            }
        });
    });

    // Reply Button Handler
    $(document).on('click', '.btn-reply', function() {
        const parentId = $(this).data('parent-id');
        $('#parent-id').val(parentId);
        $('#comment-text').focus();
    });

    loadComments();
});
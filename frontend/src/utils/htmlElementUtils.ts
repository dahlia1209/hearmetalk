export function resize(textarea: HTMLTextAreaElement) {
    textarea.style.height = 'auto';
    textarea.style.height = (textarea.scrollHeight) +1+ 'px';
};

export function sizeToHumanReadable(size) {
  let num = size;
  for (const unit of ['B', 'KB', 'MB', 'GB', 'TB']) {
    if (num < 1024) {
      return `${num.toFixed(1)} ${unit}`;
    }
    num /= (2 ** 10);
  }
  return size.toFixed(2);
}

export function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i += 1) {
      const cookie = cookies[i].trim();
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === (`${name}=`)) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

// Must be provided correct 'this' object with
//  handleStatusResponse.call(this, <argument_promise>)
export function handleStatusResponse(responsePromise) {
  return responsePromise
    .then((success) => {
      this.$root.$emit('snackbar', {
        text: success.data,
        color: 'success',
      });
    })
    .catch((error) => {
      this.$root.$emit('snackbar', {
        text: `${error.name}: ${error.message}`,
        color: 'error',
      });
    });
}

export function getFileExtension(file) {
  return file.name.split('.').pop();
}

export function isAllowedType(filename, allowedTypes) {
  const ext = getFileExtension(filename);
  return allowedTypes.includes(ext.toLowerCase());
}

export default {
  sizeToHumanReadable,
  getCookie,
  handleStatusResponse,
};

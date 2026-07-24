import { ref } from 'vue'

const toasts = ref([])
let nextId = 1

export function useToasts() {
  function addToast(message, type = 'error') {
    const id = nextId++
    toasts.value.push({ id, message, type })
    setTimeout(() => removeToast(id), 5000)
  }

  function removeToast(id) {
    toasts.value = toasts.value.filter((toast) => toast.id !== id)
  }

  return { toasts, addToast, removeToast }
}

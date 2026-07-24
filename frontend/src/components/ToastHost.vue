<script setup>
import { useToasts } from '../composables/useToasts'

const { toasts, removeToast } = useToasts()
</script>

<template>
  <div class="toast-host">
    <div
      v-for="toast in toasts"
      :key="toast.id"
      class="toast"
      :class="toast.type"
      @click="removeToast(toast.id)"
    >
      {{ toast.message }}
    </div>
  </div>
</template>

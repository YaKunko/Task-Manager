<script setup>
import { useTasksStore } from '../stores/tasks'

const store = useTasksStore()
</script>

<template>
  <div v-if="store.pages > 1" class="pagination">
    <button
      class="btn"
      :disabled="store.page <= 1 || store.loading"
      @click="store.setPage(store.page - 1)"
    >
      ← Prev
    </button>
    <span class="page-info">Page {{ store.page }} of {{ store.pages }}</span>
    <button
      class="btn"
      :disabled="store.page >= store.pages || store.loading"
      @click="store.setPage(store.page + 1)"
    >
      Next →
    </button>
  </div>
</template>

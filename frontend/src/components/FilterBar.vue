<script setup>
import { ref, watch } from 'vue'
import { useTasksStore } from '../stores/tasks'

const store = useTasksStore()

const STATUS_TABS = [
  { value: '', label: 'All' },
  { value: 'pending', label: 'Pending' },
  { value: 'in_progress', label: 'In Progress' },
  { value: 'completed', label: 'Completed' },
]

const SORT_OPTIONS = [
  { value: 'created_at:desc', label: 'Newest first' },
  { value: 'created_at:asc', label: 'Oldest first' },
  { value: 'deadline:asc', label: 'Deadline (soonest)' },
  { value: 'deadline:desc', label: 'Deadline (latest)' },
]

const searchInput = ref(store.search)
let debounceTimer = null

watch(searchInput, (value) => {
  clearTimeout(debounceTimer)
  debounceTimer = setTimeout(() => store.setSearch(value.trim()), 300)
})

function onSortChange(event) {
  const [sortBy, sortOrder] = event.target.value.split(':')
  store.setSort(sortBy, sortOrder)
}
</script>

<template>
  <div class="filter-bar">
    <nav class="status-tabs">
      <button
        v-for="tab in STATUS_TABS"
        :key="tab.value"
        class="tab"
        :class="{ active: store.status === tab.value }"
        @click="store.setStatus(tab.value)"
      >
        {{ tab.label }}
      </button>
    </nav>
    <input
      v-model="searchInput"
      class="input search-input"
      type="search"
      placeholder="Search by title..."
    />
    <select class="input" :value="`${store.sortBy}:${store.sortOrder}`" @change="onSortChange">
      <option v-for="option in SORT_OPTIONS" :key="option.value" :value="option.value">
        {{ option.label }}
      </option>
    </select>
  </div>
</template>

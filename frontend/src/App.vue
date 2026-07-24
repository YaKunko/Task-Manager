<script setup>
import { onMounted, ref } from 'vue'
import { useTasksStore } from './stores/tasks'
import TaskCard from './components/TaskCard.vue'
import ToastHost from './components/ToastHost.vue'
import FilterBar from './components/FilterBar.vue'
import PaginationBar from './components/PaginationBar.vue'
import TaskFormModal from './components/TaskFormModal.vue'

const store = useTasksStore()
const showForm = ref(false)
const editingTask = ref(null)

function openCreateForm() {
  editingTask.value = null
  showForm.value = true
}

function openEditForm(task) {
  editingTask.value = task
  showForm.value = true
}

onMounted(() => store.fetchTasks())
</script>

<template>
  <div class="app">
    <header class="app-header">
      <div>
        <h1>Task Manager</h1>
        <p class="subtitle">{{ store.total }} tasks</p>
      </div>
      <button class="btn btn-primary" @click="openCreateForm">+ New Task</button>
    </header>

    <FilterBar />

    <div v-if="store.loading" class="task-grid">
      <div v-for="n in 6" :key="n" class="skeleton-card" />
    </div>

    <div v-else-if="store.error" class="state-box error-box">
      <p>{{ store.error }}</p>
      <button class="btn" @click="store.fetchTasks()">Retry</button>
    </div>

    <div v-else-if="store.tasks.length === 0" class="state-box">
      <p>No tasks found. Create your first task!</p>
    </div>

    <div v-else class="task-grid">
      <TaskCard
        v-for="task in store.tasks"
        :key="task.id"
        :task="task"
        @edit="openEditForm"
      />
    </div>

    <PaginationBar />

    <TaskFormModal
      v-if="showForm"
      :task="editingTask"
      :key="editingTask?.id ?? 'new'"
      @close="showForm = false"
    />

    <ToastHost />
  </div>
</template>

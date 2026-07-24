<script setup>
import { computed } from 'vue'
import { useTasksStore } from '../stores/tasks'
import { useToasts } from '../composables/useToasts'

const props = defineProps({ task: { type: Object, required: true } })
const emit = defineEmits(['edit'])

const store = useTasksStore()
const { addToast } = useToasts()

const STATUS_LABELS = {
  pending: 'Pending',
  in_progress: 'In Progress',
  completed: 'Completed',
}

const isOverdue = computed(
  () =>
    props.task.deadline &&
    props.task.status !== 'completed' &&
    new Date(props.task.deadline) < new Date()
)

function formatDate(iso) {
  return new Date(iso).toLocaleString(undefined, {
    dateStyle: 'medium',
    timeStyle: 'short',
  })
}

async function changeStatus(event) {
  try {
    await store.updateTask(props.task.id, { status: event.target.value })
    addToast('Status updated', 'success')
  } catch (error) {
    addToast(error.message)
  }
}

async function removeTask() {
  if (!window.confirm(`Delete task "${props.task.title}"?`)) return
  try {
    await store.removeTask(props.task.id)
    addToast('Task deleted', 'success')
  } catch (error) {
    addToast(error.message)
  }
}
</script>

<template>
  <article class="task-card" :class="{ completed: task.status === 'completed' }">
    <div class="card-top">
      <span class="badge" :class="`status-${task.status}`">
        {{ STATUS_LABELS[task.status] }}
      </span>
      <span class="badge" :class="`priority-${task.priority}`">
        {{ task.priority }}
      </span>
    </div>
    <h3 class="card-title">{{ task.title }}</h3>
    <p v-if="task.description" class="card-description">{{ task.description }}</p>
    <p class="card-deadline" :class="{ overdue: isOverdue }">
      <template v-if="task.deadline">
        Due {{ formatDate(task.deadline) }}<span v-if="isOverdue"> — overdue</span>
      </template>
      <template v-else>No deadline</template>
    </p>
    <footer class="card-footer">
      <select class="input status-select" :value="task.status" @change="changeStatus">
        <option value="pending">Pending</option>
        <option value="in_progress">In Progress</option>
        <option value="completed">Completed</option>
      </select>
      <div class="card-actions">
        <button class="btn btn-ghost" @click="emit('edit', task)">Edit</button>
        <button class="btn btn-ghost btn-danger" @click="removeTask">Delete</button>
      </div>
    </footer>
  </article>
</template>

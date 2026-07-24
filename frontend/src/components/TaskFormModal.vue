<script setup>
import { reactive, ref } from 'vue'
import { useTasksStore } from '../stores/tasks'
import { useToasts } from '../composables/useToasts'

const props = defineProps({ task: { type: Object, default: null } })
const emit = defineEmits(['close'])

const store = useTasksStore()
const { addToast } = useToasts()

function toLocalInputValue(iso) {
  if (!iso) return ''
  const date = new Date(iso)
  const offsetMs = date.getTimezoneOffset() * 60000
  return new Date(date.getTime() - offsetMs).toISOString().slice(0, 16)
}

const form = reactive({
  title: props.task?.title ?? '',
  description: props.task?.description ?? '',
  status: props.task?.status ?? 'pending',
  priority: props.task?.priority ?? 'medium',
  deadline: toLocalInputValue(props.task?.deadline),
})

const titleError = ref('')
const saving = ref(false)

async function submit() {
  const title = form.title.trim()
  if (!title) {
    titleError.value = 'Title is required'
    return
  }
  if (title.length > 200) {
    titleError.value = 'Title must be at most 200 characters'
    return
  }
  titleError.value = ''

  const payload = {
    title,
    description: form.description.trim() || null,
    status: form.status,
    priority: form.priority,
    deadline: form.deadline ? new Date(form.deadline).toISOString() : null,
  }

  saving.value = true
  try {
    if (props.task) {
      await store.updateTask(props.task.id, payload)
      addToast('Task updated', 'success')
    } else {
      await store.createTask(payload)
      addToast('Task created', 'success')
    }
    emit('close')
  } catch (error) {
    addToast(error.message)
  } finally {
    saving.value = false
  }
}
</script>

<template>
  <div class="modal-overlay" @click.self="emit('close')">
    <div class="modal">
      <h2>{{ props.task ? 'Edit Task' : 'New Task' }}</h2>
      <form @submit.prevent="submit">
        <label class="field">
          <span>Title *</span>
          <input
            v-model="form.title"
            class="input"
            type="text"
            placeholder="What needs to be done?"
          />
          <span v-if="titleError" class="field-error">{{ titleError }}</span>
        </label>
        <label class="field">
          <span>Description</span>
          <textarea
            v-model="form.description"
            class="input"
            rows="3"
            placeholder="Optional details..."
          />
        </label>
        <div class="field-row">
          <label class="field">
            <span>Status</span>
            <select v-model="form.status" class="input">
              <option value="pending">Pending</option>
              <option value="in_progress">In Progress</option>
              <option value="completed">Completed</option>
            </select>
          </label>
          <label class="field">
            <span>Priority</span>
            <select v-model="form.priority" class="input">
              <option value="low">Low</option>
              <option value="medium">Medium</option>
              <option value="high">High</option>
            </select>
          </label>
        </div>
        <label class="field">
          <span>Deadline</span>
          <input v-model="form.deadline" class="input" type="datetime-local" />
        </label>
        <div class="modal-actions">
          <button type="button" class="btn" @click="emit('close')">Cancel</button>
          <button type="submit" class="btn btn-primary" :disabled="saving">
            {{ saving ? 'Saving...' : props.task ? 'Save Changes' : 'Create Task' }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

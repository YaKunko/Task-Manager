import { defineStore } from 'pinia'
import { tasksApi } from '../api/tasks'

export const useTasksStore = defineStore('tasks', {
  state: () => ({
    tasks: [],
    total: 0,
    pages: 0,
    page: 1,
    pageSize: 9,
    status: '',
    search: '',
    sortBy: 'created_at',
    sortOrder: 'desc',
    loading: false,
    error: null,
  }),
  actions: {
    async fetchTasks() {
      this.loading = true
      this.error = null
      try {
        const data = await tasksApi.list({
          status: this.status,
          search: this.search,
          sort_by: this.sortBy,
          sort_order: this.sortOrder,
          page: this.page,
          page_size: this.pageSize,
        })
        if (data.pages > 0 && this.page > data.pages) {
          this.page = data.pages
          return await this.fetchTasks()
        }
        this.tasks = data.items
        this.total = data.total
        this.pages = data.pages
      } catch (error) {
        this.error = error.message
      } finally {
        this.loading = false
      }
    },
    setStatus(status) {
      this.status = status
      this.page = 1
      this.fetchTasks()
    },
    setSearch(search) {
      this.search = search
      this.page = 1
      this.fetchTasks()
    },
    setSort(sortBy, sortOrder) {
      this.sortBy = sortBy
      this.sortOrder = sortOrder
      this.page = 1
      this.fetchTasks()
    },
    setPage(page) {
      this.page = page
      this.fetchTasks()
    },
    async createTask(data) {
      await tasksApi.create(data)
      await this.fetchTasks()
    },
    async updateTask(id, data) {
      await tasksApi.update(id, data)
      await this.fetchTasks()
    },
    async removeTask(id) {
      await tasksApi.remove(id)
      await this.fetchTasks()
    },
  },
})

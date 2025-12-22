'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/lib/auth';
import { api } from '@/lib/api';

interface Task {
  id: number;
  user_id: string;
  title: string;
  description?: string;
  completed: boolean;
  created_at: string;
  updated_at: string;
}

export default function TasksPage() {
  const router = useRouter();
  const { user, isLoading } = useAuth();
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [filter, setFilter] = useState<'all' | 'pending' | 'completed'>('all');
  const [showAddForm, setShowAddForm] = useState(false);
  const [newTask, setNewTask] = useState({ title: '', description: '' });
  const [editingTask, setEditingTask] = useState<Task | null>(null);

  // Redirect if not authenticated
  useEffect(() => {
    if (!isLoading && !user) {
      router.push('/');
    }
  }, [isLoading, user, router]);

  // Fetch tasks when user is loaded
  useEffect(() => {
    if (user) {
      loadTasks();
    }
  }, [user]);

  const loadTasks = async () => {
    if (!user) return;
    try {
      setLoading(true);
      const data = await api.getTasks(user.id);
      setTasks(data);
      setError(null);
    } catch (err: any) {
      setError(err.message || 'Failed to load tasks');
    } finally {
      setLoading(false);
    }
  };

  const handleAddTask = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!user || !newTask.title.trim()) return;

    try {
      await api.createTask(user.id, {
        title: newTask.title,
        description: newTask.description || undefined
      });
      setNewTask({ title: '', description: '' });
      setShowAddForm(false);
      loadTasks();
    } catch (err: any) {
      setError(err.message || 'Failed to add task');
    }
  };

  const handleUpdateTask = async (taskId: number, updates: Partial<Task>) => {
    if (!user) return;
    try {
      await api.updateTask(user.id, taskId, updates);
      loadTasks();
      setEditingTask(null);
    } catch (err: any) {
      setError(err.message || 'Failed to update task');
    }
  };

  const handleDeleteTask = async (taskId: number) => {
    if (!user || !confirm('Delete this task?')) return;
    try {
      await api.deleteTask(user.id, taskId);
      loadTasks();
    } catch (err: any) {
      setError(err.message || 'Failed to delete task');
    }
  };

  const handleToggleComplete = async (taskId: number) => {
    if (!user) return;
    try {
      await api.toggleTaskComplete(user.id, taskId);
      loadTasks();
    } catch (err: any) {
      setError(err.message || 'Failed to update task');
    }
  };

  const filteredTasks = tasks.filter(task => {
    if (filter === 'pending') return !task.completed;
    if (filter === 'completed') return task.completed;
    return true;
  });

  if (isLoading || loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-neon-dark">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-neon-cyan shadow-[0_0_15px_#00f3ff]"></div>
      </div>
    );
  }

  if (!user) return null;

  return (
    <main className="min-h-screen bg-neon-dark circuit-bg p-8">
      <div className="scanline" />
      
      <div className="max-w-6xl mx-auto relative z-10">
        {/* Header */}
        <div className="glass-card p-6 neon-border mb-8">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-4xl font-bold tracking-tighter heading-robotic glow-pulse">
                TASK NEXUS
              </h1>
              <p className="text-gray-400 text-sm font-mono mt-1">
                [MANUAL_INTERFACE] // Direct task manipulation
              </p>
            </div>
            <div className="flex gap-3">
              <button
                onClick={() => router.push('/chat')}
                className="btn border-neon-magenta text-neon-magenta px-6 py-3 text-sm"
              >
                AI Chat →
              </button>
              <button
                onClick={() => setShowAddForm(true)}
                className="btn btn-primary px-6 py-3"
              >
                + New Task
              </button>
            </div>
          </div>
        </div>

        {/* Filters */}
        <div className="glass-card p-4 neon-border-magenta mb-6 flex gap-4">
          <button
            onClick={() => setFilter('all')}
            className={`px-4 py-2 rounded-lg font-mono text-xs transition-all ${
              filter === 'all'
                ? 'bg-neon-cyan/20 text-neon-cyan border border-neon-cyan/50'
                : 'text-gray-400 hover:text-white'
            }`}
          >
            ALL [{tasks.length}]
          </button>
          <button
            onClick={() => setFilter('pending')}
            className={`px-4 py-2 rounded-lg font-mono text-xs transition-all ${
              filter === 'pending'
                ? 'bg-neon-magenta/20 text-neon-magenta border border-neon-magenta/50'
                : 'text-gray-400 hover:text-white'
            }`}
          >
            PENDING [{tasks.filter(t => !t.completed).length}]
          </button>
          <button
            onClick={() => setFilter('completed')}
            className={`px-4 py-2 rounded-lg font-mono text-xs transition-all ${
              filter === 'completed'
                ? 'bg-neon-lime/20 text-neon-lime border border-neon-lime/50'
                : 'text-gray-400 hover:text-white'
            }`}
          >
            COMPLETED [{tasks.filter(t => t.completed).length}]
          </button>
        </div>

        {/* Error Message */}
        {error && (
          <div className="bg-red-500/10 border border-red-500/30 text-red-500 px-4 py-3 rounded-lg mb-6 font-mono text-sm">
            [ERROR] {error}
          </div>
        )}

        {/* Add Task Form */}
        {showAddForm && (
          <div className="glass-card p-6 neon-border mb-6 animate-in fade-in slide-in-from-bottom-4">
            <form onSubmit={handleAddTask} className="space-y-4">
              <h3 className="robotic-tag mb-4">New Task Entry</h3>
              <input
                type="text"
                placeholder="TASK TITLE..."
                value={newTask.title}
                onChange={(e) => setNewTask({ ...newTask, title: e.target.value })}
                className="input w-full bg-white/5 border-neon-cyan/20 focus:border-neon-cyan uppercase font-mono text-sm"
                required
              />
              <textarea
                placeholder="DESCRIPTION (OPTIONAL)..."
                value={newTask.description}
                onChange={(e) => setNewTask({ ...newTask, description: e.target.value })}
                className="input w-full bg-white/5 border-neon-cyan/20 focus:border-neon-cyan uppercase font-mono text-sm h-24"
              />
              <div className="flex gap-3">
                <button
                  type="button"
                  onClick={() => {
                    setShowAddForm(false);
                    setNewTask({ title: '', description: '' });
                  }}
                  className="btn border-white/10 text-gray-400 px-6"
                >
                  Cancel
                </button>
                <button type="submit" className="btn btn-primary flex-1">
                  Create Task
                </button>
              </div>
            </form>
          </div>
        )}

        {/* Tasks List */}
        <div className="space-y-4">
          {filteredTasks.length === 0 ? (
            <div className="glass-card p-12 text-center">
              <p className="text-gray-500 font-mono text-sm">
                [NO_TASKS] // {filter === 'all' ? 'Create your first task' : `No ${filter} tasks found`}
              </p>
            </div>
          ) : (
            filteredTasks.map((task) => (
              <div
                key={task.id}
                className={`glass-card p-6 neon-border hover:border-neon-cyan transition-all group ${
                  task.completed ? 'opacity-60' : ''
                }`}
              >
                {editingTask?.id === task.id ? (
                  <div className="space-y-4">
                    <input
                      type="text"
                      value={editingTask.title}
                      onChange={(e) => setEditingTask({ ...editingTask, title: e.target.value })}
                      className="input w-full bg-white/5 border-neon-cyan/20 focus:border-neon-cyan uppercase font-mono text-sm"
                    />
                    <textarea
                      value={editingTask.description || ''}
                      onChange={(e) => setEditingTask({ ...editingTask, description: e.target.value })}
                      className="input w-full bg-white/5 border-neon-cyan/20 focus:border-neon-cyan uppercase font-mono text-sm h-20"
                    />
                    <div className="flex gap-3">
                      <button
                        onClick={() => setEditingTask(null)}
                        className="btn border-white/10 text-gray-400 px-4 text-xs"
                      >
                        Cancel
                      </button>
                      <button
                        onClick={() => handleUpdateTask(task.id, { title: editingTask.title, description: editingTask.description })}
                        className="btn btn-primary px-4 text-xs"
                      >
                        Save
                      </button>
                    </div>
                  </div>
                ) : (
                  <div className="flex items-start gap-4">
                    <input
                      type="checkbox"
                      checked={task.completed}
                      onChange={() => handleToggleComplete(task.id)}
                      className="mt-1 h-5 w-5 rounded accent-neon-cyan cursor-pointer"
                    />
                    <div className="flex-1">
                      <h3 className={`text-lg font-bold mb-1 ${task.completed ? 'line-through text-gray-600' : 'text-white'}`}>
                        {task.title}
                      </h3>
                      {task.description && (
                        <p className="text-sm text-gray-400 mb-2">{task.description}</p>
                      )}
                      <p className="text-[10px] text-gray-600 font-mono">
                        ID: {task.id} // CREATED: {new Date(task.created_at).toLocaleDateString()}
                      </p>
                    </div>
                    <div className="flex gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
                      <button
                        onClick={() => setEditingTask(task)}
                        className="text-neon-cyan hover:text-white text-xs font-mono px-3 py-1 border border-neon-cyan/30 hover:border-neon-cyan rounded transition-all"
                      >
                        EDIT
                      </button>
                      <button
                        onClick={() => handleDeleteTask(task.id)}
                        className="text-red-500 hover:text-red-300 text-xs font-mono px-3 py-1 border border-red-500/30 hover:border-red-500 rounded transition-all"
                      >
                        DELETE
                      </button>
                    </div>
                  </div>
                )}
              </div>
            ))
          )}
        </div>
      </div>
    </main>
  );
}

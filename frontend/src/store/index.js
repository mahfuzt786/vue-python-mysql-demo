import Vue from 'vue';
import Vuex from 'vuex';
import axios from 'axios';

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    token: null,
    user: null,
    errors: null,
    users: [],
    workbook: null,
  },
  mutations: {
    setToken(state, token) {
      state.token = token;
    },
    setUser(state, user) {
      state.user = user;
    },
    setUsers(state, users) {
      state.users = users;
    },
    setWorkbook(state, workbook) {
      state.workbook = workbook;
    },
    setErrors(state, errors) {
      state.errors = errors;
    },
  },
  actions: {
    async login({ commit }, { email, password }) {
      try {
          const response = await axios.post('http://127.0.0.1:8001/api/login', { email, password });
          console.log(response);
          
          const token = response.data.token; // Adjusted to match your backend response
          const user = response.data.user; // user data is returned
          commit('setToken', token);
          commit('setUser', user); // Uncomment if user data is returned
          commit('setErrors', '');
          return token;
      } catch (error) {
          if (error.response) {
              if (error.response.status === 401) {
                  commit('setErrors', 'Invalid email or password. Please try again.');
              } else {
                  commit('setErrors', error.response.data.message || 'An error occurred');
              }
          } else if (error.request) {
              commit('setErrors', 'No response from the server. Please try again later.');
          } else {
              commit('setErrors', 'Error: ' + error.message);
          }
          return false;
      }
    },  
    async register({ commit }, { name, email, address, password, contactNumber }) {
        try {
            const response = await axios.post('http://127.0.0.1:8001/api/register', { name, email, address, password, contactNumber });
            const message = response.data.message;
    
            commit('setErrors', '');
            return message;
        } catch (error) {
            if (error.response) {
                if (error.response.status === 409) {
                    commit('setErrors', 'Email already registered');
                } else {
                    commit('setErrors', error.response.data.message || 'An error occurred');
                }
            } else if (error.request) {
                commit('setErrors', 'No response from the server');
            } else {
                commit('setErrors', 'Error: ' + error.message);
            }
            return false;
        }
    },  
    async fetchUsers({ commit }) {
        try {
            const response = await axios.get('http://127.0.0.1:8001/api/users', {
                headers: {
                    Authorization: `Bearer ${this.state.token}`,
                },
            });
            commit('setUsers', response.data);
            return response.data;
        } catch (error) {
            if (error.response) {
                if (error.response.status === 401) {
                    commit('setErrors', 'Unauthorized. Please log in again.');
                } else {
                    commit('setErrors', error.response.data.message || 'An error occurred');
                }
            } else if (error.request) {
                commit('setErrors', 'No response from the server');
            } else {
                commit('setErrors', 'Error: ' + error.message);
            }
        }
    },    
    async createUser(_, { name, email, address, password, contactNumber }) {
        try {
            const response = await axios.post(`http://127.0.0.1:8001/api/users`, { name, email, address, password, contactNumber }, {
                headers: {
                    Authorization: `Bearer ${this.state.token}`,
                },
            });
            return response.data;
        } catch (error) {
            if (error.response) {
                if (error.response.status === 401) {
                    console.error('Unauthorized. Please log in again.');
                } else if (error.response.status === 403) {
                    console.error('Permission denied');
                } else {
                    console.error(error.response.data.message || 'An error occurred');
                }
            } else if (error.request) {
                console.error('No response from the server');
            } else {
                console.error('Error: ' + error.message);
            }
        }
    },    
    async updateUser(_, user) {
        try {
            const response = await axios.put(`http://127.0.0.1:8001/api/users/${user.id}`, user, {
                headers: {
                    Authorization: `Bearer ${this.state.token}`,
                },
            });
            return response.data;
        } catch (error) {
            if (error.response) {
                if (error.response.status === 401) {
                    console.error('Unauthorized. Please log in again.');
                } else if (error.response.status === 403) {
                    console.error('Permission denied');
                } else {
                    console.error(error.response.data.message || 'An error occurred');
                }
            } else if (error.request) {
                console.error('No response from the server');
            } else {
                console.error('Error: ' + error.message);
            }
        }
    },    
    async deleteUser(_, userId) {
        try {
            await axios.delete(`http://127.0.0.1:8001/api/users/${userId}`, {
                headers: {
                    Authorization: `Bearer ${this.state.token}`,
                },
            });
        } catch (error) {
            if (error.response) {
                if (error.response.status === 401) {
                    console.error('Unauthorized. Please log in again.');
                } else if (error.response.status === 403) {
                    console.error('Permission denied');
                } else {
                    console.error(error.response.data.message || 'An error occurred');
                }
            } else if (error.request) {
                console.error('No response from the server');
            } else {
                console.error('Error: ' + error.message);
            }
        }
    },
    // async fetchRecords() {
    //     this.loading = true;
    //     try {
    //       const response = await axios.get('http://127.0.0.1:8001/api/combined-transactions', {
    //         params: {
    //           page: this.page,
    //           per_page: this.itemsPerPage,
    //         },
    //       });
    //       this.records = response.data.records;
    //       this.totalRecords = response.data.totalRecords;
    //     } catch (error) {
    //       console.error('Error fetching records:', error);
    //     } finally {
    //       this.loading = false;
    //     }
    // },
    
  },
  getters: {
    isAuthenticated(state) {
      return !!state.token;
    },
    user(state) {
      return state.user;
    },
    errors(state) {
      return state.errors;
    }
  }
});

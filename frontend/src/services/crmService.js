import api from './api';

export const getLeads = async (params = {}) => (await api.get('/leads', { params })).data;
export const createLead = async (payload) => (await api.post('/leads', payload)).data;
export const getPipeline = async () => (await api.get('/reports/lead-pipeline')).data;
export const getSalesSummary = async () => (await api.get('/reports/sales-summary')).data;

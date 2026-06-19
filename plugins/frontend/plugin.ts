import type { RouteRecordRaw } from 'vue-router'

export interface LabPlugin {
  id: string
  title: string
  routePrefix: string
  routes: RouteRecordRaw[]
  apiBase: string
}

export const plugin: LabPlugin = {
  id: 'edu.cn.gov.bid-graph',
  title: 'Bid Relationship Graph Simulation',
  routePrefix: '/labs/edu.cn.gov.bid-graph',
  routes: [{ path: '', component: () => import('./BidGraphLab.vue') }],
  apiBase: '/api/v1/labs/edu.cn.gov.bid-graph',
}

export default plugin

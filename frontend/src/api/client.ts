import axios from "axios"

import type { CategoryAmount, MonthlyPoint } from "../types"

const api = axios.create({ baseURL: "/api" })

export async function getByCategory(): Promise<CategoryAmount[]> {
  const { data } = await api.get("/analytics/by-category")
  return data
}

export async function getMonthly(): Promise<MonthlyPoint[]> {
  const { data } = await api.get("/analytics/monthly")
  return data
}

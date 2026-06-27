import { CategoryPie } from "./components/CategoryPie"
import { MonthlyChart } from "./components/MonthlyChart"

export default function App() {
  return (
    <div className="app">
      <h1>FinSight</h1>
      <div className="grid">
        <CategoryPie />
        <MonthlyChart />
      </div>
    </div>
  )
}

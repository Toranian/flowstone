"use client";

// import { useState } from "react";
import { Bar, BarChart, ResponsiveContainer, XAxis, YAxis } from "recharts";
import {
  Bell,
  // Calendar,
  Clock,
  // Layout,
  // List,
  // Settings,
  // User,
} from "lucide-react";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import {
  ChartContainer,
  ChartTooltip,
  ChartTooltipContent,
} from "@/components/ui/chart";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import AreaChartComponent from "@/components/AreaChart";

// Filler data for the chart
const chartData = [
  { day: "Mon", hours: 5 },
  { day: "Tue", hours: 7 },
  { day: "Wed", hours: 6 },
  { day: "Thu", hours: 8 },
  { day: "Fri", hours: 6 },
  { day: "Sat", hours: 4 },
  { day: "Sun", hours: 2 },
];

// Filler data for recent time entries
const recentEntries = [
  { id: 1, task: "Project A", duration: "2h 15m", date: "2024-03-10" },
  { id: 2, task: "Meeting", duration: "1h 30m", date: "2024-03-10" },
  { id: 3, task: "Project B", duration: "3h 45m", date: "2024-03-09" },
  { id: 4, task: "Email", duration: "45m", date: "2024-03-09" },
  { id: 5, task: "Project C", duration: "4h", date: "2024-03-08" },
];

export default function TimeDashboard() {
  // const [activeNav, setActiveNav] = useState("dashboard");

  return (
    <div className="flex h-screen bg-gray-100">
      {/* Sidebar */}
      {/* <aside className="w-64 bg-white p-4 shadow-md"> */}
      {/*   <nav className="space-y-2"> */}
      {/*     {[ */}
      {/*       { name: "Dashboard", icon: Layout }, */}
      {/*       { name: "Time Entries", icon: List }, */}
      {/*       { name: "Calendar", icon: Calendar }, */}
      {/*       { name: "Reports", icon: Clock }, */}
      {/*       { name: "Settings", icon: Settings }, */}
      {/*       { name: "Profile", icon: User }, */}
      {/*     ].map((item) => ( */}
      {/*       <button */}
      {/*         key={item.name} */}
      {/*         className={`flex items-center space-x-2 w-full p-2 rounded-lg text-left ${ */}
      {/*           activeNav === item.name.toLowerCase() */}
      {/*             ? "bg-gray-200" */}
      {/*             : "hover:bg-gray-100" */}
      {/*         }`} */}
      {/*         onClick={() => setActiveNav(item.name.toLowerCase())} */}
      {/*       > */}
      {/*         <item.icon className="h-5 w-5" /> */}
      {/*         <span>{item.name}</span> */}
      {/*       </button> */}
      {/*     ))} */}
      {/*   </nav> */}
      {/* </aside> */}

      {/* Main content */}
      <main className="flex-1 p-2 md:p-8 overflow-auto">
        <div className="max-w-5xl mx-auto space-y-8">
          {/* <h1 className="text-3xl font-bold">Focus Tracking Dashboard</h1> */}
          {/* Metrics */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">
                  Total Hours This Week
                </CardTitle>
                <Clock className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">38 hours</div>
                <p className="text-xs text-muted-foreground">
                  +2.5% from last week
                </p>
              </CardContent>
            </Card>
            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">
                  Average Daily Hours
                </CardTitle>
                <Clock className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">5.4 hours</div>
                <p className="text-xs text-muted-foreground">
                  -0.3 hours from last week
                </p>
              </CardContent>
            </Card>
            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">
                  Distractions
                </CardTitle>
                <Bell className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">12</div>
                <p className="text-xs text-muted-foreground">
                  -25% from last week
                </p>
              </CardContent>
            </Card>
          </div>
          {/* Chart */}
          <Card>
            <CardHeader>
              <CardTitle className="text-xl">Focused Hours of Work</CardTitle>
              <CardDescription>
                Your daily work hours for the past week
              </CardDescription>
            </CardHeader>
            <CardContent className="pt-4">
              <ChartContainer
                config={{
                  hours: {
                    label: "Hours",
                    color: "hsl(var(--chart-2))",
                  },
                }}
                className="h-[300px] w-full"
              >
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={chartData}>
                    <XAxis dataKey="day" />
                    <YAxis />
                    <ChartTooltip content={<ChartTooltipContent />} />
                    <Bar
                      dataKey="hours"
                      fill="var(--color-hours)"
                      radius={[4, 4, 0, 0]}
                    />
                  </BarChart>
                </ResponsiveContainer>
              </ChartContainer>
            </CardContent>
          </Card>

          <AreaChartComponent />

          {/* Recent Time Entries */}
          <Card>
            <CardHeader>
              <CardTitle className="text-xl">Recent Time Entries</CardTitle>
              <CardDescription>Your latest recorded activities</CardDescription>
            </CardHeader>
            <CardContent>
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>Task</TableHead>
                    <TableHead>Duration</TableHead>
                    <TableHead>Date</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {recentEntries.map((entry) => (
                    <TableRow key={entry.id}>
                      <TableCell>{entry.task}</TableCell>
                      <TableCell>{entry.duration}</TableCell>
                      <TableCell>{entry.date}</TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </CardContent>
          </Card>
        </div>
      </main>
    </div>
  );
}

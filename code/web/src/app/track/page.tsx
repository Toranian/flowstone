"use client";

import { useState, useEffect } from "react";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";

export default function ClockCountdownTimer() {
  const [time, setTime] = useState({ hours: 0, minutes: 0, seconds: 0 });
  const [running, setRunning] = useState(false);
  const [inputTime, setInputTime] = useState({
    hours: "0",
    minutes: "0",
    seconds: "0",
  });
  const [progress, setProgress] = useState(100);
  const [totalSeconds, setTotalSeconds] = useState(0);

  useEffect(() => {
    let interval: NodeJS.Timeout | null = null;

    if (running) {
      interval = setInterval(() => {
        setTime((prevTime) => {
          if (
            prevTime.hours === 0 &&
            prevTime.minutes === 0 &&
            prevTime.seconds === 0
          ) {
            setRunning(false);
            return prevTime;
          }

          const newSeconds = prevTime.seconds - 1;
          const newMinutes =
            newSeconds < 0 ? prevTime.minutes - 1 : prevTime.minutes;
          const newHours = newMinutes < 0 ? prevTime.hours - 1 : prevTime.hours;

          const newTime = {
            hours: newHours,
            minutes: newMinutes < 0 ? 59 : newMinutes,
            seconds: newSeconds < 0 ? 59 : newSeconds,
          };

          const elapsedSeconds =
            totalSeconds -
            (newTime.hours * 3600 + newTime.minutes * 60 + newTime.seconds);
          setProgress(((totalSeconds - elapsedSeconds) / totalSeconds) * 100);

          return newTime;
        });
      }, 1000);
    }

    return () => {
      if (interval) clearInterval(interval);
    };
  }, [running, totalSeconds]);

  const startTimer = () => {
    const seconds =
      parseInt(inputTime.hours) * 3600 +
      parseInt(inputTime.minutes) * 60 +
      parseInt(inputTime.seconds);

    if (seconds > 0) {
      setTime({
        hours: parseInt(inputTime.hours),
        minutes: parseInt(inputTime.minutes),
        seconds: parseInt(inputTime.seconds),
      });
      setTotalSeconds(seconds);
      setProgress(100);
      setRunning(true);
    }
  };

  const stopTimer = () => {
    setRunning(false);
  };

  const resetTimer = () => {
    setRunning(false);
    setTime({ hours: 0, minutes: 0, seconds: 0 });
    setInputTime({ hours: "0", minutes: "0", seconds: "0" });
    setProgress(100);
    setTotalSeconds(0);
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setInputTime((prev) => ({ ...prev, [name]: value }));
  };

  const radius = 120;
  const circumference = 2 * Math.PI * radius;
  const strokeDashoffset = circumference - (progress / 100) * circumference;

  return (
    <Card className="w-[350px]">
      <CardHeader>
        <CardTitle>Countdown Timer</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="grid grid-cols-3 gap-4 mb-4">
          <div className="flex flex-col">
            <Label htmlFor="hours">Hours</Label>
            <Input
              id="hours"
              name="hours"
              type="number"
              min="0"
              value={inputTime.hours}
              onChange={handleInputChange}
              disabled={running}
            />
          </div>
          <div className="flex flex-col">
            <Label htmlFor="minutes">Minutes</Label>
            <Input
              id="minutes"
              name="minutes"
              type="number"
              min="0"
              max="59"
              value={inputTime.minutes}
              onChange={handleInputChange}
              disabled={running}
            />
          </div>
          <div className="flex flex-col">
            <Label htmlFor="seconds">Seconds</Label>
            <Input
              id="seconds"
              name="seconds"
              type="number"
              min="0"
              max="59"
              value={inputTime.seconds}
              onChange={handleInputChange}
              disabled={running}
            />
          </div>
        </div>
        <div className="relative w-64 h-64 mx-auto">
          <svg className="w-full h-full" viewBox="0 0 256 256">
            <circle
              cx="128"
              cy="128"
              r={radius}
              fill="none"
              stroke="hsl(var(--muted))"
              strokeWidth="8"
            />
            <circle
              cx="128"
              cy="128"
              r={radius}
              fill="none"
              stroke="hsl(var(--primary))"
              strokeWidth="8"
              strokeDasharray={circumference}
              strokeDashoffset={strokeDashoffset}
              strokeLinecap="round"
              transform="rotate(-90 128 128)"
            />
          </svg>
          <div className="absolute top-0 left-0 w-full h-full flex items-center justify-center">
            <div className="text-4xl font-bold text-center" aria-live="polite">
              {String(time.hours).padStart(2, "0")}:
              {String(time.minutes).padStart(2, "0")}:
              {String(time.seconds).padStart(2, "0")}
            </div>
          </div>
        </div>
      </CardContent>
      <CardFooter className="flex justify-between">
        <Button onClick={startTimer} disabled={running}>
          Start
        </Button>
        <Button onClick={stopTimer} disabled={!running}>
          Stop
        </Button>
        <Button onClick={resetTimer}>Reset</Button>
      </CardFooter>
    </Card>
  );
}

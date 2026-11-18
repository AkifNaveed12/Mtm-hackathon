Create a shadcn component variant in the codebase.

The codebase should support following:

- Shadcn project structure
- React ^19
- Tailwind CSS ^4
- TypeScript ^5

If it doesn't, provide instructions on how to setup project via shadcn CLI, install Tailwind CSS v4 or Typescript.

Dependencies:

```bash
npm install @dnd-kit/core @dnd-kit/sortable @dnd-kit/utilities @base-ui/react react-dom
```

Shadcn Registry Dependencies:

```bash
npx shadcn@latest add button badge utils
```

Copy-paste this file to `components/shadcn-studio/kanban` folder:

```tsx
kanban-01.tsx
'use client'

import type { ComponentProps } from 'react'
import { useState } from 'react'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import {
  Kanban,
  KanbanBoard,
  KanbanColumn,
  KanbanColumnContent,
  KanbanColumnHandle,
  KanbanItem,
  KanbanItemHandle,
  KanbanOverlay
} from '@/components/ui/kanban'

import { cn } from '@/lib/utils'
import { CalendarIcon, GripVerticalIcon } from 'lucide-react'

type Priority = 'low' | 'medium' | 'high'
type ColumnId = 'todo' | 'inProgress' | 'done'

interface Task {
  id: string
  title: string
  priority: Priority
  dueDate: string
  label: string
}

const COLUMN_META: Record<ColumnId, { title: string; subtitle: string; accent: string }> = {
  todo: {
    title: 'Todo',
    subtitle: 'Next up',
    accent: 'bg-slate-400'
  },
  inProgress: {
    title: 'In Progress',
    subtitle: 'Being worked',
    accent: 'bg-blue-500'
  },
  done: {
    title: 'Done',
    subtitle: 'Completed',
    accent: 'bg-emerald-500'
  }
}

const PRIORITY_STYLES: Record<Priority, string> = {
  low: 'bg-emerald-500',
  medium: 'bg-amber-500',
  high: 'bg-rose-500'
}

const INITIAL_COLUMNS: Record<ColumnId, Task[]> = {
  todo: [
    {
      id: 'task-1',
      title: 'Design onboarding flow',
      priority: 'high',
      dueDate: 'Jun 15',
      label: 'Product'
    },
    {
      id: 'task-2',
      title: 'Write API docs',
      priority: 'medium',
      dueDate: 'Jun 18',
      label: 'Docs'
    },
    {
      id: 'task-3',
      title: 'Define data schema',
      priority: 'low',
      dueDate: 'Jun 22',
      label: 'Backend'
    }
  ],
  inProgress: [
    {
      id: 'task-4',
      title: 'Implement auth module',
      priority: 'high',
      dueDate: 'Jun 14',
      label: 'Security'
    },
    {
      id: 'task-5',
      title: 'Build REST endpoints',
      priority: 'medium',
      dueDate: 'Jun 16',
      label: 'API'
    },
    {
      id: 'task-6',
      title: 'Dark mode support',
      priority: 'medium',
      dueDate: 'Jun 17',
      label: 'UI'
    }
  ],
  done: [
    {
      id: 'task-7',
      title: 'Project setup and scaffolding',
      priority: 'high',
      dueDate: 'Jun 01',
      label: 'Setup'
    },
    {
      id: 'task-8',
      title: 'Initial DB migrations',
      priority: 'low',
      dueDate: 'Jun 02',
      label: 'Database'
    }
  ]
}

interface TaskCardProps extends Omit<ComponentProps<typeof KanbanItem>, 'value' | 'children'> {
  task: Task
  isOverlay?: boolean
}

function TaskCard({ task, isOverlay, ...props }: TaskCardProps) {
  const card = (
    <div
      className={cn(
        'bg-background rounded-lg border p-3 shadow-xs transition-all',
        !isOverlay && 'hover:border-primary/30 hover:shadow-sm',
        isOverlay && 'ring-primary/20 rotate-1 shadow-lg ring-2'
      )}
    >
      <div className='mb-3 flex items-center justify-between gap-2'>
        <span className='bg-muted text-muted-foreground rounded-md px-2 py-0.5 text-xs font-medium'>{task.label}</span>
        <span className='text-muted-foreground flex items-center gap-1 text-xs whitespace-nowrap tabular-nums'>
          <CalendarIcon className='size-3' />
          {task.dueDate}
        </span>
      </div>
      <div className='flex items-start gap-2.5'>
        <span className={cn('mt-1.5 size-2 shrink-0 rounded-full', PRIORITY_STYLES[task.priority])} />
        <p className='line-clamp-2 text-sm leading-snug font-medium'>{task.title}</p>
      </div>
    </div>
  )

  return (
    <KanbanItem value={task.id} {...props}>
      {isOverlay ? card : <KanbanItemHandle>{card}</KanbanItemHandle>}
    </KanbanItem>
  )
}

interface TaskColumnProps extends Omit<ComponentProps<typeof KanbanColumn>, 'children' | 'value'> {
  value: ColumnId
  tasks: Task[]
  isOverlay?: boolean
}

function TaskColumn({ value, tasks, isOverlay, ...props }: TaskColumnProps) {
  const meta = COLUMN_META[value]

  return (
    <KanbanColumn value={value} {...props}>
      <div className='bg-muted flex h-full flex-col rounded-xl border p-2'>
        <div className='flex items-center justify-between px-3 pt-2 pb-4'>
          <div className='flex min-w-0 items-center gap-2'>
            <h3 className='text-sm font-semibold'>{meta.title}</h3>
            <Badge variant='outline'>{tasks.length}</Badge>
          </div>
          <KanbanColumnHandle
            render={handleProps => (
              <Button {...handleProps} size='icon-xs' variant='ghost' aria-label={`Move ${meta.title} column`}>
                <GripVerticalIcon />
              </Button>
            )}
          />
        </div>
        <KanbanColumnContent value={value} className='gap-2.5'>
          {tasks.map(task => (
            <TaskCard key={task.id} task={task} isOverlay={isOverlay} />
          ))}
        </KanbanColumnContent>
      </div>
    </KanbanColumn>
  )
}

const KanbanDemo = () => {
  const [columns, setColumns] = useState<Record<string, Task[]>>(INITIAL_COLUMNS)

  return (
    <div className='space-y-4 overflow-x-auto'>
      <Kanban
        value={columns}
        onValueChange={setColumns}
        getItemValue={item => item.id}
        className='mx-auto w-full max-w-4xl'
      >
        <KanbanBoard className='grid auto-rows-fr grid-cols-[repeat(3,minmax(14rem,1fr))] gap-3'>
          {Object.entries(columns).map(([columnId, tasks]) => (
            <TaskColumn key={columnId} value={columnId as ColumnId} tasks={tasks} />
          ))}
        </KanbanBoard>
        <KanbanOverlay>
          {({ value, variant }) => {
            const activeValue = String(value)

            if (variant === 'column') {
              return <TaskColumn value={activeValue as ColumnId} tasks={columns[activeValue] ?? []} isOverlay />
            }

            const task = Object.values(columns)
              .flat()
              .find(t => t.id === activeValue)

            return task ? <TaskCard task={task} isOverlay /> : null
          }}
        </KanbanOverlay>
      </Kanban>

      <p className='text-muted-foreground text-center text-xs'>
        Inspired by{' '}
        <a
          className='hover:text-foreground underline'
          href='https://reui.io/components/kanban'
          target='_blank'
          rel='noopener noreferrer'
        >
          ReUI
        </a>
      </p>
    </div>
  )
}

export default KanbanDemo
```

Copy-paste this file to `components/ui` folder:

```tsx
kanban.tsx;
("use client");

import * as React from "react";

import type { CSSProperties, ReactNode } from "react";
import {
  createContext,
  useCallback,
  useContext,
  useLayoutEffect,
  useMemo,
  useRef,
  useState,
} from "react";

import { mergeProps } from "@base-ui/react/merge-props";
import { useRender } from "@base-ui/react/use-render";

import type {
  DragEndEvent,
  DragOverEvent,
  DragStartEvent,
  DropAnimation,
  Modifiers,
  UniqueIdentifier,
  DraggableAttributes,
  DraggableSyntheticListeners,
} from "@dnd-kit/core";

import {
  DndContext,
  DragOverlay,
  KeyboardSensor,
  MeasuringStrategy,
  PointerSensor,
  useSensor,
  useSensors,
  defaultDropAnimationSideEffects,
} from "@dnd-kit/core";

import {
  arrayMove,
  defaultAnimateLayoutChanges,
  rectSortingStrategy,
  SortableContext,
  sortableKeyboardCoordinates,
  useSortable,
  verticalListSortingStrategy,
  type AnimateLayoutChanges,
} from "@dnd-kit/sortable";
import { CSS } from "@dnd-kit/utilities";
import { createPortal } from "react-dom";

import { cn } from "@/lib/utils";

// Stable module-level constants — never recreated, won't trigger dnd-kit effects
const measuringConfig = {
  droppable: { strategy: MeasuringStrategy.Always },
};

const pointerActivationConstraint = { distance: 10 };

interface KanbanContextProps<T> {
  columns: Record<string, T[]>;
  setColumns: (columns: Record<string, T[]>) => void;
  getItemId: (item: T) => string;
  columnIds: string[];
  activeId: UniqueIdentifier | null;
  setActiveId: (id: UniqueIdentifier | null) => void;
  findContainer: (id: UniqueIdentifier) => string | undefined;
  isColumn: (id: UniqueIdentifier) => boolean;
  modifiers?: Modifiers;
}

const KanbanContext = createContext<KanbanContextProps<any>>({
  columns: {},
  setColumns: () => {},
  getItemId: () => "",
  columnIds: [],
  activeId: null,
  setActiveId: () => {},
  findContainer: () => undefined,
  isColumn: () => false,
  modifiers: undefined,
});

const ColumnContext = createContext<{
  attributes: DraggableAttributes;
  listeners: DraggableSyntheticListeners | undefined;
  isDragging?: boolean;
  disabled?: boolean;
}>({
  attributes: {} as DraggableAttributes,
  listeners: undefined,
  isDragging: false,
  disabled: false,
});

const ItemContext = createContext<{
  listeners: DraggableSyntheticListeners | undefined;
  isDragging?: boolean;
  disabled?: boolean;
}>({
  listeners: undefined,
  isDragging: false,
  disabled: false,
});

const IsOverlayContext = createContext(false);

const animateLayoutChanges: AnimateLayoutChanges = (args) =>
  defaultAnimateLayoutChanges({ ...args, wasDragging: true });

const dropAnimationConfig: DropAnimation = {
  sideEffects: defaultDropAnimationSideEffects({
    styles: { active: { opacity: "0.4" } },
  }),
};

export interface KanbanMoveEvent {
  event: DragEndEvent;
  activeContainer: string;
  activeIndex: number;
  overContainer: string;
  overIndex: number;
}

export interface KanbanRootProps<T> extends Omit<
  useRender.ComponentProps<"div">,
  "children"
> {
  value: Record<string, T[]>;
  onValueChange: (value: Record<string, T[]>) => void;
  getItemValue: (item: T) => string;
  children: ReactNode;
  onMove?: (event: KanbanMoveEvent) => void;
  modifiers?: Modifiers;
}

function Kanban<T>({
  value,
  onValueChange,
  getItemValue,
  children,
  className,
  render,
  onMove,
  modifiers,
  ...props
}: KanbanRootProps<T>) {
  const columns = value;
  const setColumns = onValueChange;
  const [activeId, setActiveId] = useState<UniqueIdentifier | null>(null);

  // Refs so all callbacks read the latest values without being recreated on every render.
  // This breaks the cascade: columns change → callbacks recreate → DndContext re-registers → loop.
  const columnsRef = useRef(columns);

  columnsRef.current = columns;

  const getItemValueRef = useRef(getItemValue);

  getItemValueRef.current = getItemValue;

  const onMoveRef = useRef(onMove);

  onMoveRef.current = onMove;

  // Sensor config objects are stable module-level constants, so useSensors result is stable.
  const sensors = useSensors(
    useSensor(PointerSensor, {
      activationConstraint: pointerActivationConstraint,
    }),
    useSensor(KeyboardSensor, {
      coordinateGetter: sortableKeyboardCoordinates,
    }),
  );

  const columnIds = useMemo(() => Object.keys(columns), [columns]);

  // isColumn only depends on columnIds (the keys, not the item arrays). Column keys don't
  // change when items are moved, so columnIds array values are stable during drags.
  const isColumn = useCallback(
    (id: UniqueIdentifier) => columnIds.includes(id as string),
    [columnIds],
  );

  // findContainer reads columnsRef so it doesn't need columns or getItemValue in its deps.
  const findContainer = useCallback(
    (id: UniqueIdentifier) => {
      if (isColumn(id)) return id as string;
      const cols = columnsRef.current;
      const getId = getItemValueRef.current;

      return Object.keys(cols).find((key) =>
        cols[key].some((item) => getId(item) === id),
      );
    },
    [isColumn],
  );

  const handleDragStart = useCallback((event: DragStartEvent) => {
    setActiveId(event.active.id);
  }, []);

  // RAF refs throttle onDragOver: we only process the latest event per animation frame.
  // This prevents React from receiving dozens of setState calls per frame during rapid drags,
  // which is what causes "Maximum update depth exceeded".
  const dragOverRafRef = useRef<number | null>(null);
  const pendingDragOverRef = useRef<DragOverEvent | null>(null);

  const handleDragOver = useCallback(
    (event: DragOverEvent) => {
      if (onMoveRef.current) return;

      // Always capture the latest event; only one RAF runs at a time.
      pendingDragOverRef.current = event;
      if (dragOverRafRef.current !== null) return;

      dragOverRafRef.current = requestAnimationFrame(() => {
        dragOverRafRef.current = null;
        const latestEvent = pendingDragOverRef.current;

        pendingDragOverRef.current = null;
        if (!latestEvent) return;

        const { active, over } = latestEvent;

        if (!over) return;
        if (isColumn(active.id)) return;

        const activeContainer = findContainer(active.id);
        const overContainer = findContainer(over.id);

        // Only reorder within the same column during drag. Cross-column moves are
        // committed in onDragEnd instead — moving an item to another column unmounts
        // its DOM node and remounts it, which releases pointer capture and causes the
        // drag to end prematurely when the kanban is rendered inside an iframe.
        if (
          !activeContainer ||
          !overContainer ||
          activeContainer !== overContainer
        )
          return;

        const cols = columnsRef.current;
        const getId = getItemValueRef.current;
        const activeIndex = cols[activeContainer].findIndex(
          (item: T) => getId(item) === active.id,
        );
        const overIndex = cols[activeContainer].findIndex(
          (item: T) => getId(item) === over.id,
        );

        if (activeIndex === overIndex) return;

        setColumns({
          ...cols,
          [activeContainer]: arrayMove(
            cols[activeContainer],
            activeIndex,
            overIndex,
          ),
        });
      });
    },
    [findContainer, isColumn, setColumns],
  );

  const flushPendingDragOver = useCallback(() => {
    if (dragOverRafRef.current !== null) {
      cancelAnimationFrame(dragOverRafRef.current);
      dragOverRafRef.current = null;
    }

    pendingDragOverRef.current = null;
  }, []);

  const handleDragCancel = useCallback(() => {
    flushPendingDragOver();
    setActiveId(null);
  }, [flushPendingDragOver]);

  const handleDragEnd = useCallback(
    (event: DragEndEvent) => {
      flushPendingDragOver();

      const { active, over } = event;

      setActiveId(null);

      if (!over) return;

      if (onMoveRef.current && !isColumn(active.id)) {
        const cols = columnsRef.current;
        const getId = getItemValueRef.current;
        const activeContainer = findContainer(active.id);
        const overContainer = findContainer(over.id);

        if (activeContainer && overContainer) {
          const activeIndex = cols[activeContainer].findIndex(
            (item: T) => getId(item) === active.id,
          );

          const overIndex = isColumn(over.id)
            ? cols[overContainer].length
            : cols[overContainer].findIndex(
                (item: T) => getId(item) === over.id,
              );

          onMoveRef.current({
            event,
            activeContainer,
            activeIndex,
            overContainer,
            overIndex,
          });
        }

        return;
      }

      if (isColumn(active.id) && isColumn(over.id)) {
        const cols = columnsRef.current;
        const keys = Object.keys(cols);
        const activeIndex = keys.indexOf(active.id as string);
        const overIndex = keys.indexOf(over.id as string);

        if (activeIndex !== overIndex) {
          const newOrder = arrayMove(keys, activeIndex, overIndex);
          const newColumns: Record<string, T[]> = {};

          newOrder.forEach((key) => {
            newColumns[key] = cols[key];
          });

          setColumns(newColumns);
        }

        return;
      }

      const activeContainer = findContainer(active.id);
      const overContainer = findContainer(over.id);

      if (!activeContainer || !overContainer) return;

      const cols = columnsRef.current;
      const getId = getItemValueRef.current;
      const activeIndex = cols[activeContainer].findIndex(
        (item: T) => getId(item) === active.id,
      );

      if (activeContainer === overContainer) {
        const overIndex = cols[overContainer].findIndex(
          (item: T) => getId(item) === over.id,
        );

        if (activeIndex !== overIndex) {
          setColumns({
            ...cols,
            [activeContainer]: arrayMove(
              cols[activeContainer],
              activeIndex,
              overIndex,
            ),
          });
        }

        return;
      }

      const overItems = cols[overContainer];

      const overIndex = isColumn(over.id)
        ? overItems.length
        : overItems.findIndex((item: T) => getId(item) === over.id);

      const newActiveItems = [...cols[activeContainer]];
      const newOverItems = [...overItems];
      const [movedItem] = newActiveItems.splice(activeIndex, 1);

      newOverItems.splice(overIndex, 0, movedItem);

      setColumns({
        ...cols,
        [activeContainer]: newActiveItems,
        [overContainer]: newOverItems,
      });
    },
    [findContainer, isColumn, setColumns, flushPendingDragOver],
  );

  // Stable getItemId wrapper so context consumers don't re-render when the parent
  // passes a new inline arrow function reference.
  const stableGetItemId = useCallback(
    (item: T) => getItemValueRef.current(item),
    [],
  );

  const contextValue = useMemo(
    () => ({
      columns,
      setColumns,
      getItemId: stableGetItemId,
      columnIds,
      activeId,
      setActiveId,
      findContainer,
      isColumn,
      modifiers,
    }),
    [
      columns,
      setColumns,
      stableGetItemId,
      columnIds,
      activeId,
      findContainer,
      isColumn,
      modifiers,
    ],
  );

  const defaultProps = {
    "data-slot": "kanban",
    "data-dragging": activeId !== null,
    className: cn(activeId !== null && "cursor-grabbing!", className),
    children,
  };

  return (
    <KanbanContext.Provider value={contextValue}>
      <DndContext
        sensors={sensors}
        modifiers={modifiers}
        measuring={measuringConfig}
        onDragStart={handleDragStart}
        onDragOver={handleDragOver}
        onDragEnd={handleDragEnd}
        onDragCancel={handleDragCancel}
      >
        {useRender({
          defaultTagName: "div",
          render,
          props: mergeProps<"div">(defaultProps, props),
        })}
      </DndContext>
    </KanbanContext.Provider>
  );
}

export type KanbanBoardProps = useRender.ComponentProps<"div">;

function KanbanBoard({ className, render, ...props }: KanbanBoardProps) {
  const { columnIds } = useContext(KanbanContext);

  const defaultProps = {
    "data-slot": "kanban-board",
    className: cn("grid auto-rows-fr gap-4 sm:grid-cols-3", className),
    children: props.children,
  };

  return (
    <SortableContext items={columnIds} strategy={rectSortingStrategy}>
      {useRender({
        defaultTagName: "div",
        render,
        props: mergeProps<"div">(defaultProps, props),
      })}
    </SortableContext>
  );
}

export interface KanbanColumnProps extends useRender.ComponentProps<"div"> {
  value: string;
  disabled?: boolean;
}

function KanbanColumn({
  value,
  className,
  render,
  disabled,
  ...props
}: KanbanColumnProps) {
  const isOverlay = useContext(IsOverlayContext);

  const {
    setNodeRef,
    transform,
    transition,
    attributes,
    listeners,
    isDragging: isSortableDragging,
  } = useSortable({
    id: value,
    disabled: disabled || isOverlay,
    animateLayoutChanges,
  });

  if (isOverlay) {
    const defaultProps = {
      "data-slot": "kanban-column",
      "data-value": value,
      "data-dragging": true,
      className: cn("group/kanban-column flex flex-col", className),
      children: props.children,
    };

    return (
      <ColumnContext.Provider
        value={{
          attributes: {} as DraggableAttributes,
          listeners: undefined,
          isDragging: true,
          disabled: false,
        }}
      >
        {useRender({
          defaultTagName: "div",
          render,
          props: mergeProps<"div">(defaultProps, props),
        })}
      </ColumnContext.Provider>
    );
  }

  const { activeId, isColumn } = useContext(KanbanContext);
  const isColumnDragging = activeId ? isColumn(activeId) : false;

  const style = {
    transition,
    transform: CSS.Transform.toString(transform),
  } as CSSProperties;

  const defaultProps = {
    "data-slot": "kanban-column",
    "data-value": value,
    "data-dragging": isSortableDragging,
    "data-disabled": disabled,
    ref: setNodeRef,
    style,
    className: cn(
      "group/kanban-column flex flex-col",
      isSortableDragging && "opacity-50 z-50",
      disabled && "opacity-50",
      className,
    ),
    children: props.children,
  };

  return (
    <ColumnContext.Provider
      value={{ attributes, listeners, isDragging: isColumnDragging, disabled }}
    >
      {useRender({
        defaultTagName: "div",
        render,
        props: mergeProps<"div">(defaultProps, props),
      })}
    </ColumnContext.Provider>
  );
}

export interface KanbanColumnHandleProps extends useRender.ComponentProps<"div"> {
  cursor?: boolean;
}

function KanbanColumnHandle({
  className,
  render,
  cursor = true,
  ...props
}: KanbanColumnHandleProps) {
  const { attributes, listeners, isDragging, disabled } =
    useContext(ColumnContext);

  const defaultProps = {
    "data-slot": "kanban-column-handle",
    "data-dragging": isDragging,
    "data-disabled": disabled,
    suppressHydrationWarning: true,
    ...attributes,
    ...listeners,
    className: cn(
      "opacity-0 transition-opacity group-hover/kanban-column:opacity-100",
      cursor && (isDragging ? "cursor-grabbing!" : "cursor-grab!"),
      className,
    ),
    children: props.children,
  };

  return useRender({
    defaultTagName: "div",
    render,
    props: mergeProps<"div">(defaultProps, props),
  });
}

export interface KanbanItemProps extends useRender.ComponentProps<"div"> {
  value: string;
  disabled?: boolean;
}

function KanbanItem({
  value,
  className,
  render,
  disabled,
  ...props
}: KanbanItemProps) {
  const isOverlay = useContext(IsOverlayContext);

  const {
    setNodeRef,
    transform,
    transition,
    attributes,
    listeners,
    isDragging: isSortableDragging,
  } = useSortable({
    id: value,
    disabled: disabled || isOverlay,
    animateLayoutChanges,
  });

  if (isOverlay) {
    const defaultProps = {
      "data-slot": "kanban-item",
      "data-value": value,
      "data-dragging": true,
      className: cn(className),
      children: props.children,
    };

    return (
      <ItemContext.Provider
        value={{ listeners: undefined, isDragging: true, disabled: false }}
      >
        {useRender({
          defaultTagName: "div",
          render,
          props: mergeProps<"div">(defaultProps, props),
        })}
      </ItemContext.Provider>
    );
  }

  const { activeId, isColumn } = useContext(KanbanContext);
  const isItemDragging = activeId ? !isColumn(activeId) : false;

  const style = {
    transition,
    transform: CSS.Transform.toString(transform),
  } as CSSProperties;

  const defaultProps = {
    "data-slot": "kanban-item",
    "data-value": value,
    "data-dragging": isSortableDragging,
    "data-disabled": disabled,
    suppressHydrationWarning: true,
    ref: setNodeRef,
    style,
    ...attributes,
    className: cn(
      isSortableDragging && "opacity-50 z-50",
      disabled && "opacity-50",
      className,
    ),
    children: props.children,
  };

  return (
    <ItemContext.Provider
      value={{ listeners, isDragging: isItemDragging, disabled }}
    >
      {useRender({
        defaultTagName: "div",
        render,
        props: mergeProps<"div">(defaultProps, props),
      })}
    </ItemContext.Provider>
  );
}

export interface KanbanItemHandleProps extends useRender.ComponentProps<"div"> {
  cursor?: boolean;
}

function KanbanItemHandle({
  className,
  render,
  cursor = true,
  ...props
}: KanbanItemHandleProps) {
  const { listeners, isDragging, disabled } = useContext(ItemContext);

  const defaultProps = {
    "data-slot": "kanban-item-handle",
    "data-dragging": isDragging,
    "data-disabled": disabled,
    ...listeners,
    className: cn(
      cursor && (isDragging ? "cursor-grabbing!" : "cursor-grab!"),
      className,
    ),
    children: props.children,
  };

  return useRender({
    defaultTagName: "div",
    render,
    props: mergeProps<"div">(defaultProps, props),
  });
}

export interface KanbanColumnContentProps extends useRender.ComponentProps<"div"> {
  value: string;
}

function KanbanColumnContent({
  value,
  className,
  render,
  ...props
}: KanbanColumnContentProps) {
  const { columns, getItemId } = useContext(KanbanContext);

  const itemIds = useMemo(
    () => columns[value].map(getItemId),
    [columns, getItemId, value],
  );

  const defaultProps = {
    "data-slot": "kanban-column-content",
    className: cn("flex flex-col gap-2", className),
    children: props.children,
  };

  return (
    <SortableContext items={itemIds} strategy={verticalListSortingStrategy}>
      {useRender({
        defaultTagName: "div",
        render,
        props: mergeProps<"div">(defaultProps, props),
      })}
    </SortableContext>
  );
}

export interface KanbanOverlayProps extends Omit<
  React.ComponentProps<typeof DragOverlay>,
  "children"
> {
  children?:
    | ReactNode
    | ((params: {
        value: UniqueIdentifier;
        variant: "column" | "item";
      }) => ReactNode);
}

function KanbanOverlay({ children, className, ...props }: KanbanOverlayProps) {
  const { activeId, isColumn, modifiers } = useContext(KanbanContext);
  const [mounted, setMounted] = useState(false);

  useLayoutEffect(() => setMounted(true), []);

  const variant = activeId ? (isColumn(activeId) ? "column" : "item") : "item";

  const content =
    activeId && children
      ? typeof children === "function"
        ? children({ value: activeId, variant })
        : children
      : null;

  if (!mounted) return null;

  return createPortal(
    <DragOverlay
      dropAnimation={dropAnimationConfig}
      modifiers={modifiers}
      className={cn("z-50", activeId && "cursor-grabbing", className)}
      {...props}
    >
      <IsOverlayContext.Provider value={true}>
        {content}
      </IsOverlayContext.Provider>
    </DragOverlay>,
    document.body,
  );
}

export {
  Kanban,
  KanbanBoard,
  KanbanColumn,
  KanbanColumnHandle,
  KanbanItem,
  KanbanItemHandle,
  KanbanColumnContent,
  KanbanOverlay,
};
```

Instructions to follow:

- Install all listed dependencies and devDependencies using package manager used in the project (npm, yarn, pnpm, etc.)
- Install the required shadcn/ui components using the shadcn CLI using package manager used in the project (npx, pnpm dlx, bunx --bun, etc.)
- Add any CSS variables and styles to the `globals.css` file of this project (just add styles that are listed, no need to add extra styles or variables)
- Create the files with the exact paths provided
- Ensure all imports are correctly configured
- The component should be fully functional and styled according to the provided code
- Now you can use this component in current project

Important: File paths for components, utils, ui, lib, and hooks may vary depending on the project structure. Always check the project's `components.json` file to determine the correct import paths and folder structure. Update all import statements and file paths in the provided code to match the project's configuration before implementing the component.

npx shadcn@latest add @ss-components/kanban-01

'use client'

import type { ComponentProps } from 'react'
import { useState } from 'react'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import {
Kanban,
KanbanBoard,
KanbanColumn,
KanbanColumnContent,
KanbanColumnHandle,
KanbanItem,
KanbanItemHandle,
KanbanOverlay
} from '@/components/ui/kanban'

import { cn } from '@/lib/utils'
import { CalendarIcon, GripVerticalIcon } from 'lucide-react'

type Priority = 'low' | 'medium' | 'high'
type ColumnId = 'todo' | 'inProgress' | 'done'

interface Task {
id: string
title: string
priority: Priority
dueDate: string
label: string
}

const COLUMN_META: Record<ColumnId, { title: string; subtitle: string; accent: string }> = {
todo: {
title: 'Todo',
subtitle: 'Next up',
accent: 'bg-slate-400'
},
inProgress: {
title: 'In Progress',
subtitle: 'Being worked',
accent: 'bg-blue-500'
},
done: {
title: 'Done',
subtitle: 'Completed',
accent: 'bg-emerald-500'
}
}

const PRIORITY_STYLES: Record<Priority, string> = {
low: 'bg-emerald-500',
medium: 'bg-amber-500',
high: 'bg-rose-500'
}

const INITIAL_COLUMNS: Record<ColumnId, Task[]> = {
todo: [
{
id: 'task-1',
title: 'Design onboarding flow',
priority: 'high',
dueDate: 'Jun 15',
label: 'Product'
},
{
id: 'task-2',
title: 'Write API docs',
priority: 'medium',
dueDate: 'Jun 18',
label: 'Docs'
},
{
id: 'task-3',
title: 'Define data schema',
priority: 'low',
dueDate: 'Jun 22',
label: 'Backend'
}
],
inProgress: [
{
id: 'task-4',
title: 'Implement auth module',
priority: 'high',
dueDate: 'Jun 14',
label: 'Security'
},
{
id: 'task-5',
title: 'Build REST endpoints',
priority: 'medium',
dueDate: 'Jun 16',
label: 'API'
},
{
id: 'task-6',
title: 'Dark mode support',
priority: 'medium',
dueDate: 'Jun 17',
label: 'UI'
}
],
done: [
{
id: 'task-7',
title: 'Project setup and scaffolding',
priority: 'high',
dueDate: 'Jun 01',
label: 'Setup'
},
{
id: 'task-8',
title: 'Initial DB migrations',
priority: 'low',
dueDate: 'Jun 02',
label: 'Database'
}
]
}

interface TaskCardProps extends Omit<ComponentProps<typeof KanbanItem>, 'value' | 'children'> {
task: Task
isOverlay?: boolean
}

function TaskCard({ task, isOverlay, ...props }: TaskCardProps) {
const card = (
<div
className={cn(
'bg-background rounded-lg border p-3 shadow-xs transition-all',
!isOverlay && 'hover:border-primary/30 hover:shadow-sm',
isOverlay && 'ring-primary/20 rotate-1 shadow-lg ring-2'
)} >
<div className='mb-3 flex items-center justify-between gap-2'>
<span className='bg-muted text-muted-foreground rounded-md px-2 py-0.5 text-xs font-medium'>{task.label}</span>
<span className='text-muted-foreground flex items-center gap-1 text-xs whitespace-nowrap tabular-nums'>
<CalendarIcon className='size-3' />
{task.dueDate}
</span>
</div>
<div className='flex items-start gap-2.5'>
<span className={cn('mt-1.5 size-2 shrink-0 rounded-full', PRIORITY_STYLES[task.priority])} />
<p className='line-clamp-2 text-sm leading-snug font-medium'>{task.title}</p>
</div>
</div>
)

return (
<KanbanItem value={task.id} {...props}>
{isOverlay ? card : <KanbanItemHandle>{card}</KanbanItemHandle>}
</KanbanItem>
)
}

interface TaskColumnProps extends Omit<ComponentProps<typeof KanbanColumn>, 'children' | 'value'> {
value: ColumnId
tasks: Task[]
isOverlay?: boolean
}

function TaskColumn({ value, tasks, isOverlay, ...props }: TaskColumnProps) {
const meta = COLUMN_META[value]

return (
<KanbanColumn value={value} {...props}>
<div className='bg-muted flex h-full flex-col rounded-xl border p-2'>
<div className='flex items-center justify-between px-3 pt-2 pb-4'>
<div className='flex min-w-0 items-center gap-2'>
<h3 className='text-sm font-semibold'>{meta.title}</h3>
<Badge variant='outline'>{tasks.length}</Badge>
</div>
<KanbanColumnHandle
render={handleProps => (
<Button {...handleProps} size='icon-xs' variant='ghost' aria-label={`Move ${meta.title} column`}>
<GripVerticalIcon />
</Button>
)}
/>
</div>
<KanbanColumnContent value={value} className='gap-2.5'>
{tasks.map(task => (
<TaskCard key={task.id} task={task} isOverlay={isOverlay} />
))}
</KanbanColumnContent>
</div>
</KanbanColumn>
)
}

const KanbanDemo = () => {
const [columns, setColumns] = useState<Record<string, Task[]>>(INITIAL_COLUMNS)

return (
<div className='space-y-4 overflow-x-auto'>
<Kanban
value={columns}
onValueChange={setColumns}
getItemValue={item => item.id}
className='mx-auto w-full max-w-4xl' >
<KanbanBoard className='grid auto-rows-fr grid-cols-[repeat(3,minmax(14rem,1fr))] gap-3'>
{Object.entries(columns).map(([columnId, tasks]) => (
<TaskColumn key={columnId} value={columnId as ColumnId} tasks={tasks} />
))}
</KanbanBoard>
<KanbanOverlay>
{({ value, variant }) => {
const activeValue = String(value)

            if (variant === 'column') {
              return <TaskColumn value={activeValue as ColumnId} tasks={columns[activeValue] ?? []} isOverlay />
            }

            const task = Object.values(columns)
              .flat()
              .find(t => t.id === activeValue)

            return task ? <TaskCard task={task} isOverlay /> : null
          }}
        </KanbanOverlay>
      </Kanban>

      <p className='text-muted-foreground text-center text-xs'>
        Inspired by{' '}
        <a
          className='hover:text-foreground underline'
          href='https://reui.io/components/kanban'
          target='_blank'
          rel='noopener noreferrer'
        >
          ReUI
        </a>
      </p>
    </div>

)
}

export default KanbanDemo

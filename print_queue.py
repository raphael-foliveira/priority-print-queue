import dataclasses


@dataclasses.dataclass
class PrintJob:
    """
    Representa um trabalho de impressão com prioridade.
    Prioridades menores são mais urgentes (ex: 1 = urgente, 2 = normal).
    """

    name: str
    priority: int


class PrintQueue:
    """
    Fila de impressão com heap binário manual para gerenciar prioridades e ordem de chegada.
    """

    def __init__(self):
        self.__heap: list[tuple[int, int, PrintJob]] = []
        self.__counter: int = 0

    def __swap(self, i: int, j: int):
        self.__heap[i], self.__heap[j] = self.__heap[j], self.__heap[i]

    def __sift_up(self, idx: int):
        while idx > 0:
            parent = (idx - 1) // 2

            if self.__heap[idx] >= self.__heap[parent]:
                return

            self.__swap(idx, parent)
            idx = parent

    def __sift_down(self, idx: int):
        heap_size = len(self.__heap)
        while True:
            current_node_index = idx
            smallest_index = idx

            left_index = 2 * idx + 1
            right_index = 2 * idx + 2

            if (
                left_index < heap_size
                and self.__heap[left_index] < self.__heap[smallest_index]
            ):
                smallest_index = left_index

            if (
                right_index < heap_size
                and self.__heap[right_index] < self.__heap[smallest_index]
            ):
                smallest_index = right_index

            if smallest_index == current_node_index:
                return

            self.__swap(current_node_index, smallest_index)
            idx = smallest_index

    def add_job(self, job: PrintJob):
        entry = (job.priority, self.__counter, job)
        self.__counter += 1
        self.__heap.append(entry)
        self.__sift_up(len(self.__heap) - 1)

    def pop_job(self) -> PrintJob | None:
        if not self.__heap:
            return None
        last = len(self.__heap) - 1
        self.__swap(0, last)
        _, _, job = self.__heap.pop()
        self.__sift_down(0)
        return job

    def list_jobs(self) -> list[PrintJob]:
        return [entry[2] for entry in sorted(self.__heap)]

    def get_heap_tree_representation(
        self, index: int = 0, prefix: str = "", is_left: bool = True
    ) -> str:
        """Retorna uma representação em string da árvore do heap."""
        if index >= len(self.__heap):
            return ""

        tree_str = ""
        job_name = self.__heap[index][2].name
        priority = self.__heap[index][0]

        if prefix:
            tree_str += prefix
            tree_str += "├── (Esq)" if is_left else "└── (Dir)"

        tree_str += f"{job_name} (P:{priority})\n"

        new_prefix = prefix + ("│   " if is_left else "    ")

        left_child_index = 2 * index + 1
        right_child_index = 2 * index + 2

        has_left_child = left_child_index < len(self.__heap)
        has_right_child = right_child_index < len(self.__heap)

        if has_left_child:
            tree_str += self.get_heap_tree_representation(
                left_child_index, new_prefix, True
            )
        if has_right_child:
            tree_str += self.get_heap_tree_representation(
                right_child_index, new_prefix, not has_left_child
            )
        return tree_str

    @property
    def heap(self) -> list[tuple[int, int, PrintJob]]:
        return self.__heap


def main():
    pq = PrintQueue()
    while True:
        print("\n=== Fila de Impressão ===")
        print("1. Enviar documento")
        print("2. Ver fila de impressão")
        print("3. Imprimir próximo documento")
        print("4. Sair")
        choice = input("Escolha uma opção: ")

        if choice == "1":
            name = input("Nome do documento: ")
            pr = input("Prioridade (1=Urgente, 2=Normal): ")
            try:
                pr_value = int(pr)
                if pr_value not in [1, 2]:
                    raise ValueError()

                job = PrintJob(name, pr_value)
                pq.add_job(job)
                print(f"Documento '{name}' adicionado com prioridade {pr_value}.")
            except ValueError:
                print(
                    "Prioridade inválida. A prioridade deve ser 1 (Urgente) ou 2 (Normal)."
                )

        elif choice == "2":
            jobs = pq.list_jobs()
            if jobs:
                print(
                    "\nOrdem de impressão (ordenada por prioridade e ordem de chegada):"
                )
                for job in jobs:
                    print(f"- {job.name} (prioridade {job.priority})")
                print("\nRepresentação da Heap:")
                print(pq.get_heap_tree_representation())
            else:
                print("Fila vazia.")

        elif choice == "3":
            job = pq.pop_job()
            if job:
                print(f"Imprimindo: {job.name} (prioridade {job.priority})")
            else:
                print("Nenhum documento para imprimir.")

        elif choice == "4":
            print("Encerrando o sistema de fila de impressão.")
            break

        else:
            print("Opção inválida. Tente novamente.")


if __name__ == "__main__":
    main()

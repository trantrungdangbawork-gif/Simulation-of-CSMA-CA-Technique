import random

# ================== PARAM ==================
NUM_NODES = 3
DIFS = 3
SIFS = 2
T_SLOT = 1 
TIME_SLOTS = 200

# ================== NODE ==================
# KHỞI TẠO
class Node:
    def __init__(self, name):
        self.name = name
        self.K = 0
        self.cw = 0
        self.state = "IDLE"
        self.timer = 0
        self.done = False
        self.frozen = False

nodes = [Node(f"Node{i+1}") for i in range(NUM_NODES)]

current_tx = None
release_next = False

def fmt(text):
    return f"{text:<28}"

# ================== HEADER ==================
print("Time ".ljust(6) + "| " + " | ".join([fmt(f"Node{i+1}") for i in range(NUM_NODES)]))
print("-"*100)

# ================== SIM ==================
t = 0.0
while t < TIME_SLOTS:
    outputs = [""] * NUM_NODES
    jump_happened = False

    if release_next:
        current_tx = None
        release_next = False
    
    # CHECK IDLE
    channel_busy = current_tx is not None
    ready_nodes = []
    

    # ĐỢI DIFS
    # ===== PHASE 1 =====
    for node in nodes:
        if node.done:
            continue

        if not channel_busy:

            if node.state == "IDLE":
                node.state = "IDLE_WAIT"

            elif node.state == "IDLE_WAIT":
                node.timer = DIFS
                node.state = "DIFS"

            elif node.state == "DIFS":
                node.timer -= 1
                if node.timer == 0:
                    node.state = "POST_DIFS"
            

            # CHỌN BACKOFF
            elif node.state == "POST_DIFS":
                cw_max = (2**node.K) - 1
                node.cw = random.randint(0, max(0, cw_max))
                node.state = "BACKOFF"

            elif node.state == "BACKOFF":
                if node.frozen:
                    node.frozen = False
                else:
                    if node.cw > 0:
                        node.cw -= 1
                    else:
                        ready_nodes.append(node)
        # NẾU NHƯ CÓ NODE KHÁC ĐANG TRUYỀN, THÌ NHỮNG NODE KHÁC SẼ BỊ ĐÓNG BĂNG
        else:
            if node.state == "BACKOFF":
                node.frozen = True  
    # NẾU CÓ NHIỀU NODE CÙNG GỬI RTS SẼ GÂY RA VA CHẠM, KHÔNG NHẬN ĐƯỢC CTS
    # ===== COLLISION / RTS =====
    if not channel_busy and ready_nodes:
        if len(ready_nodes) > 1:
            # COLLISION
            for i, node in enumerate(nodes):
                if node in ready_nodes:
                    outputs[i] = "RTS collision -> no CTS"
                elif node.done:
                    outputs[i] = "done"
                else:
                    outputs[i] = f"k={node.K}, idle channel"

            print(f"{t:<6}| " + " | ".join([fmt(o) for o in outputs]))

            t += SIFS
            

            # NẾU VA CHẠM, NHỮNG NODE BỊ VA CHẠM SẼ TĂNG K LÊN 1 
            # VÀ ĐỢI THỜI GIAN BACKOFF MỚI TRƯỚC KHI THỬ GỬI LẠI
            # tăng K
            k_outputs = []
            for n in nodes:
                if n in ready_nodes:
                    n.K += 1
                    k_outputs.append(fmt(f"k={n.K-1}+1"))
                else:
                    k_outputs.append(fmt("done" if n.done else "idle"))

            print(f"{t:<6}| " + " | ".join(k_outputs))

            # TB
            tb_values = [((2**n.K) - 1) / 2 * T_SLOT for n in ready_nodes]
            tb_jump = sum(tb_values) / len(tb_values)

            if tb_jump > 0:
                t += tb_jump
                print(f"{t:<6}| " + " | ".join([
                    fmt(f"wait TB time ({tb_jump})") if n in ready_nodes
                    else fmt("done" if n.done else "idle")
                    for n in nodes
                ]))

                # idle sau TB
                idle_outputs = []
                for n in nodes:
                    if n in ready_nodes:
                        idle_outputs.append(fmt(f"k={n.K}, idle channel"))
                    else:
                        idle_outputs.append(fmt("done" if n.done else "idle"))

                print(f"{t:<6}| " + " | ".join(idle_outputs))

            # reset
            for n in ready_nodes:
                n.state = "IDLE_WAIT"
                n.frozen = False

            jump_happened = True
            continue

        else:
            node = ready_nodes[0]
            node.state = "SIFS_RTS"
            node.timer = SIFS
            current_tx = node

    # ===== PHASE 2 =====
    if not jump_happened:
        for i, node in enumerate(nodes):
            if node.done:
                outputs[i] = "done"
                continue

            if current_tx and node != current_tx:
                outputs[i] = "busy channel -> freeze"
                continue

            if node.state == "IDLE":
                outputs[i] = f"k={node.K}, idle channel"

            elif node.state == "IDLE_WAIT":
                outputs[i] = f"k={node.K}, idle channel"

            elif node.state == "DIFS":
                outputs[i] = "wait DIFS"

            elif node.state == "POST_DIFS":
                outputs[i] = "idle channel"
            
            # SAU KHI NODE ĐẾM NGƯỢC VỀ TỚI 0 SẼ GỬI RTS
            elif node.state == "BACKOFF":
                if node.cw == 0:
                    outputs[i] = f"k={node.K}, cw=0 -> sent RTS"
                else:
                    outputs[i] = f"k={node.K}, cw={node.cw}"
            # SAU KHI GỬI RTS THÀNH CÔNG, NODE SẼ CHỜ SIFS RỒI NHẬN CTS
            elif node.state == "SIFS_RTS":
                outputs[i] = "wait SIFS"
                node.timer -= 1
                if node.timer == 0:
                    node.state = "CTS"

            elif node.state == "CTS":
                outputs[i] = "RTS success -> receive CTS"
                node.state = "SIFS_CTS"
                node.timer = SIFS
            # SAU KHI NHẬN ĐƯỢC CTS, NODE SẼ CHỜ SIFS RỒI GỬI DATA
            elif node.state == "SIFS_CTS":
                outputs[i] = "wait SIFS"
                node.timer -= 1
                if node.timer == 0:
                    node.state = "DATA"
            # SAU KHI GỬI DATA, NODE SẼ CHỜ SIFS RỒI NHẬN ACK
            elif node.state == "DATA":
                outputs[i] = "send DATA"
                node.state = "SIFS_ACK"
                node.timer = SIFS

            elif node.state == "SIFS_ACK":
                outputs[i] = "wait SIFS"
                node.timer -= 1
                if node.timer == 0:
                    node.state = "ACK"
            # NẾU NHẬN ĐƯỢC ACK, NODE SẼ KẾT THÚC VÀ GIẢI PHÓNG KÊNH
            elif node.state == "ACK":
                outputs[i] = "receive ACK"
                node.state = "SUCCESS"

            elif node.state == "SUCCESS":
                outputs[i] = "success"
                node.done = True
                release_next = True

        print(f"{t:<6}| " + " | ".join([fmt(o) for o in outputs]))
        t += 1.0

    # ===== STOP =====
    if all(node.done for node in nodes):
        print("-" * 100)
        print(f"TẤT CẢ CÁC NODE ĐÃ TRUYỀN THÀNH CÔNG TẠI TIME: {t}")
        break